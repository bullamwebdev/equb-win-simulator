from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from models.params import SimulateRequest, OptimizeRequest, CascadeRequest
from models.results import SimulateResponse, OptimizeResponse, CascadeResponse
from engine.distribution import (
    win_probability_single, e_first_win_round, p_win_round1,
    p_breakeven, var_95, strategy_score, win_distribution_pmf, first_win_pmf
)
from engine.montecarlo import run_simulation
from engine.optimizer import find_optimal_M, full_parameter_sweep
from engine.cascade import cascade_self_funding
import pandas as pd
import io

app = FastAPI(title="Equb Win Simulator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "app": "Equb Win Simulator", "docs": "/docs"}

@app.post("/api/simulate", response_model=SimulateResponse)
def simulate(req: SimulateRequest):
    mc = run_simulation(req.N, req.M, req.C, req.cycles, req.n_sims)
    return SimulateResponse(
        win_pmf=win_distribution_pmf(req.M, req.N),
        first_win_pmf=first_win_pmf(req.M, req.N),
        montecarlo=mc,
        metrics={
            "e_first_win": round(e_first_win_round(req.M, req.N), 4),
            "p_win_round1": round(p_win_round1(req.M, req.N) * 100, 2),
            "p_breakeven": round(p_breakeven(req.M, req.N) * 100, 2),
            "strategy_score": round(strategy_score(req.M, req.N), 2),
            "var_95": round(var_95(req.M, req.N, req.C), 2),
            "win_probability_single": round(win_probability_single(req.N) * 100, 2)
        }
    )

@app.post("/api/optimize", response_model=OptimizeResponse)
def optimize(req: OptimizeRequest):
    return find_optimal_M(req.N, req.target_win_rate_pct, req.target_metric, req.max_M)

@app.get("/api/sweep")
def sweep(
    N_list: str = Query(default="5,10,20,50"),
    C: float = Query(default=100.0)
):
    N_vals = [int(x) for x in N_list.split(",")]
    return full_parameter_sweep(N_vals, C=C)

@app.get("/api/export/csv")
def export_csv(
    N_list: str = Query(default="5,10,20,50"),
    C: float = Query(default=100.0)
):
    N_vals = [int(x) for x in N_list.split(",")]
    data = full_parameter_sweep(N_vals, C=C)
    df = pd.DataFrame(data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=equb_sweep.csv"}
    )

@app.post("/api/cascade", response_model=CascadeResponse)
def cascade(req: CascadeRequest):
    return cascade_self_funding(req.N, req.M_start, req.C, req.n_cycles)
