from pydantic import BaseModel, Field
from typing import List, Dict

class RiskQuery(BaseModel):
    nav: float = Field(10_000_000, gt=0)
    tickers: List[str] = Field(["SPY", "QQQ", "TLT"], min_length=1)
    weights: List[float] = Field([0.5, 0.3, 0.2], min_length=1)
    confidence_level: float = Field(0.99, ge=0.90, le=0.999)
    horizon_days: int = Field(10, ge=1, le=250)

class RiskResponse(BaseModel):
    nav: float
    confidence_level: float
    horizon_days: int
    metrics: Dict
    stress_tests: Dict