from math import ceil
from scipy.stats import binom as binom_dist
import numpy as np

def win_probability_single(N: int) -> float:
    """P(win any given round) for one raffle = 1/N"""
    return 1.0 / N

def e_first_win_round(M: int, N: int) -> float:
    """E[min of M Uniform(1..N)] = Σ_{k=0}^{N-1} ((N-k)/N)^M"""
    return sum(((N - k) / N) ** M for k in range(N))

def p_win_round1(M: int, N: int) -> float:
    """P(win at least one raffle in Round 1) = 1-(1-1/N)^M"""
    return 1.0 - (1.0 - 1.0 / N) ** M

def p_breakeven(M: int, N: int) -> float:
    """P(wins >= ceil(M/N)) using Binomial CDF — break-even condition"""
    k_min = ceil(M / N)
    return float(1 - binom_dist.cdf(k_min - 1, M, 1.0 / N))

def var_95(M: int, N: int, C: float) -> float:
    """Capital at risk at 5th percentile of win distribution (VaR 95%)"""
    entry_cost = C * N
    prize = N * entry_cost
    wins_5pct = float(binom_dist.ppf(0.05, M, 1.0 / N))
    return wins_5pct * (prize - entry_cost) + (M - wins_5pct) * (-entry_cost)

def strategy_score(M: int, N: int) -> float:
    """Composite score: 0.5*p_win_round1 + 0.5*p_breakeven (scale 0-100)"""
    return 0.5 * p_win_round1(M, N) * 100 + 0.5 * p_breakeven(M, N) * 100

def win_distribution_pmf(M: int, N: int) -> list[dict]:
    """PMF of total wins: Binomial(M, 1/N)"""
    p = 1.0 / N
    return [
        {"wins": k, "probability": round(float(binom_dist.pmf(k, M, p)), 6)}
        for k in range(min(M + 1, 51))  # cap at 50 for payload size
    ]

def first_win_pmf(M: int, N: int) -> list[dict]:
    """P(first win at round k) = ((N-k+1)/N)^M - ((N-k)/N)^M"""
    result = []
    for k in range(1, N + 1):
        p = ((N - k + 1) / N) ** M - ((N - k) / N) ** M
        result.append({"round": k, "probability": round(float(p), 6)})
    return result

def heatmap_data(
    N_vals: list[int] = [5, 10, 20, 50],
    M_vals: list[int] = [1, 5, 10, 20, 50, 100, 200, 500, 1000]
) -> list[dict]:
    """Returns flat list for heatmap: {N, M, p_win_round1, p_breakeven, score}"""
    rows = []
    for N in N_vals:
        for M in M_vals:
            rows.append({
                "N": N, "M": M,
                "p_win_round1": round(p_win_round1(M, N) * 100, 2),
                "p_breakeven": round(p_breakeven(M, N) * 100, 2),
                "e_first_win": round(e_first_win_round(M, N), 3),
                "score": round(strategy_score(M, N), 2)
            })
    return rows
