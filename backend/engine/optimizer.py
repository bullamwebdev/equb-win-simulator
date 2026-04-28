from engine.distribution import (
    p_win_round1, p_breakeven, strategy_score,
    e_first_win_round, var_95
)
from models.results import OptimizeResponse

def find_optimal_M(
    N: int,
    target_win_rate_pct: float,
    target_metric: str = "p_win_round1",
    max_M: int = 1000,
    C: float = 100.0
) -> OptimizeResponse:
    """Binary search for minimum M achieving target metric >= target_win_rate_pct."""
    metric_fn = p_win_round1 if target_metric == "p_win_round1" else p_breakeven

    lo, hi = 1, max_M
    result_M = max_M

    while lo <= hi:
        mid = (lo + hi) // 2
        val = metric_fn(mid, N) * 100
        if val >= target_win_rate_pct:
            result_M = mid
            hi = mid - 1
        else:
            lo = mid + 1

    achieved = metric_fn(result_M, N) * 100
    score = strategy_score(result_M, N)
    efr = e_first_win_round(result_M, N)
    risk = var_95(result_M, N, C)

    if result_M <= N:
        rec = f"Conservative zone — M={result_M} matches group size. Win rate is moderate."
    elif result_M <= 5 * N:
        rec = f"Optimal zone — M={result_M} hits target with peak strategy score. Recommended."
    else:
        rec = f"Aggressive zone — M={result_M} guarantees target but increases capital exposure."

    return OptimizeResponse(
        optimal_M=result_M,
        achieved_value=round(achieved, 2),
        strategy_score=round(score, 2),
        e_first_win=round(efr, 4),
        var_95=round(risk, 2),
        recommendation=rec
    )

def full_parameter_sweep(
    N_range: list[int] = [5, 10, 20, 50],
    M_range: list[int] = [1, 5, 10, 20, 50, 100, 200, 500, 1000],
    C: float = 100.0
) -> list[dict]:
    """Full scenario grid for all N x M combinations."""
    rows = []
    for N in N_range:
        for M in M_range:
            entry_cost = C * N
            prize = N * entry_cost
            rows.append({
                "N": N, "M": M, "C": C,
                "entry_cost": entry_cost,
                "prize_pool": prize,
                "p_win_single_pct": round(100.0 / N, 2),
                "e_first_win_round": round(e_first_win_round(M, N), 3),
                "p_win_round1_pct": round(p_win_round1(M, N) * 100, 2),
                "p_breakeven_pct": round(p_breakeven(M, N) * 100, 2),
                "strategy_score": round(strategy_score(M, N), 2),
                "var_95": round(var_95(M, N, C), 2),
                "total_invested": M * entry_cost,
                "expected_wins": round(M / N, 2)
            })
    return rows
