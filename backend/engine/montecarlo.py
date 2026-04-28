import numpy as np

def run_simulation(
    N: int, M: int, C: float,
    cycles: int = 3,
    n_sims: int = 5000
) -> dict:
    """
    Monte Carlo cascade wealth simulation.
    Per sim: for each cycle, each round: deduct contributions, add wins.
    Returns mean, p10, p90 trajectories + cycle break indices.
    """
    total_rounds = cycles * N
    wealth = np.zeros((n_sims, total_rounds + 1))
    wealth[:, 0] = M * C  # seed capital = one round of all raffles

    rng = np.random.default_rng(seed=42)

    for t in range(1, total_rounds + 1):
        wins = rng.binomial(M, 1.0 / N, size=n_sims)
        wealth[:, t] = wealth[:, t - 1] - M * C + wins * N * C

    return {
        "rounds": list(range(total_rounds + 1)),
        "mean": [round(float(v), 2) for v in wealth.mean(axis=0)],
        "p10":  [round(float(v), 2) for v in np.percentile(wealth, 10, axis=0)],
        "p90":  [round(float(v), 2) for v in np.percentile(wealth, 90, axis=0)],
        "p25":  [round(float(v), 2) for v in np.percentile(wealth, 25, axis=0)],
        "p75":  [round(float(v), 2) for v in np.percentile(wealth, 75, axis=0)],
        "cycle_breaks": [N * i for i in range(1, cycles + 1)]
    }
