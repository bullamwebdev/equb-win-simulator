from pydantic import BaseModel, Field
from typing import Literal

class SimulateRequest(BaseModel):
    N: int = Field(default=10, ge=2, le=100, description="Group size / members per raffle")
    M: int = Field(default=50, ge=1, le=1000, description="Simultaneous raffles")
    C: float = Field(default=100.0, gt=0, description="Contribution per round")
    cycles: int = Field(default=3, ge=1, le=10)
    n_sims: int = Field(default=5000, ge=100, le=10000)

class OptimizeRequest(BaseModel):
    N: int = Field(default=10, ge=2, le=100)
    target_win_rate_pct: float = Field(default=90.0, ge=50.0, le=100.0)
    target_metric: Literal["p_win_round1", "p_breakeven"] = "p_win_round1"
    max_M: int = Field(default=1000, ge=10, le=5000)

class CascadeRequest(BaseModel):
    N: int = Field(default=10, ge=2, le=100)
    M_start: int = Field(default=10, ge=1, le=500)
    C: float = Field(default=100.0, gt=0)
    n_cycles: int = Field(default=5, ge=1, le=20)
