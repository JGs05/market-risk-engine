import duckdb
import yfinance as yf
import pandas as pd
from typing import List

class DataManager:
    def __init__(self, db_path: str = "data/market_data.duckdb"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with duckdb.connect(self.db_path) as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS asset_prices (
                    date DATE,
                    ticker VARCHAR,
                    adj_close DOUBLE,
                    PRIMARY KEY (date, ticker)
                );
            """)

    def ingest_tickers(self, tickers: List[str], start_date: str = "2007-01-01", end_date: str = "2024-01-01"):
        raw = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)["Close"]
        df_long = raw.reset_index().melt(id_vars=["Date"], var_name="ticker", value_name="adj_close")
        df_long.rename(columns={"Date": "date"}, inplace=True)
        df_long.dropna(inplace=True)

        with duckdb.connect(self.db_path) as con:
            con.register("temp_df", df_long)
            con.execute("""
                INSERT OR REPLACE INTO asset_prices
                SELECT CAST(date AS DATE), ticker, CAST(adj_close AS DOUBLE)
                FROM temp_df;
            """)
        print(f"Successfully ingested {len(tickers)} tickers into {self.db_path}")

    def fetch_return_matrix(self, tickers: List[str]) -> pd.DataFrame:
        placeholders = ",".join([f"'{t}'" for t in tickers])
        query = f"""
            SELECT date, ticker, adj_close
            FROM asset_prices
            WHERE ticker IN ({placeholders})
            ORDER BY date ASC;
        """
        with duckdb.connect(self.db_path) as con:
            df = con.execute(query).df()
        
        pivoted = df.pivot(index="date", columns="ticker", values="adj_close")
        returns = pivoted.pct_change().dropna()
        return returns