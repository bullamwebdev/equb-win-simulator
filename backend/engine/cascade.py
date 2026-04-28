from engine.distribution import e_first_win_round, p_win_round1
from models.results import CascadeResponse
import numpy as np

def cascade_self_funding(
    N: int, M_start: int, C: float, n_cycles: int = 5
) -> CascadeResponse:
    """
    Simulate self-funding cascade over n_cycles.
    First win proceeds are reinvested as additional raffle entries.
    """
    rng = np.random.default_rng(42)
    M = float(M_start)
    capital = M_start * C
    cycles_list = []
    M_growth = []
    cum_capital = []
    rounds_self_funded = -1

    entry_cost = C * N
    prize = N * entry_cost

    for cycle in range(1, n_cycles + 1):
        for rd in range(1, N + 1):
            wins = rng.binomial(int(M), 1.0 / N)
            capital = capital - int(M) * C + wins * prize

        # Reinvest: additional entries funded by net gain
        new_entries = max(0.0, capital / entry_cost - M)
        M = M + new_entries * 0.5  # reinvest 50% of surplus into new raffles

        cycles_list.append(cycle)
        M_growth.append(round(M, 2))
        cum_capital.append(round(capital, 2))

        if rounds_self_funded == -1 and capital >= M_start * entry_cost * n_cycles:
            rounds_self_funded = cycle

    return CascadeResponse(
        cycles=cycles_list,
        M_growth=M_growth,
        cumulative_capital=cum_capital,
        rounds_until_self_funded=rounds_self_funded if rounds_self_funded != -1 else n_cycles
    )
