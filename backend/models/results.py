from pydantic import BaseModel
from typing import Any

class SimulateResponse(BaseModel):
    win_pmf: list[dict]
    first_win_pmf: list[dict]
    montecarlo: dict
    metrics: dict

class OptimizeResponse(BaseModel):
    optimal_M: int
    achieved_value: float
    strategy_score: float
    e_first_win: float
    var_95: float
    recommendation: str

class CascadeResponse(BaseModel):
    cycles: list[int]
    M_growth: list[float]
    cumulative_capital: list[float]
    rounds_until_self_funded: int
