import pytest
from engine.distribution import (
    win_probability_single, e_first_win_round, p_win_round1,
    p_breakeven, strategy_score, win_distribution_pmf, first_win_pmf
)

def test_win_probability_single():
    assert win_probability_single(10) == pytest.approx(0.1)
    assert win_probability_single(5) == pytest.approx(0.2)

def test_e_first_win_round_single_raffle():
    # With M=1, expected first win = (N+1)/2
    assert e_first_win_round(1, 10) == pytest.approx(5.5, rel=1e-3)

def test_e_first_win_round_large_M():
    # With very large M, first win should be near 1
    assert e_first_win_round(1000, 10) == pytest.approx(1.0, abs=0.01)

def test_p_win_round1_bounds():
    assert 0 < p_win_round1(10, 10) < 1
    assert p_win_round1(1000, 10) == pytest.approx(1.0, abs=0.001)

def test_p_breakeven_single():
    # Single raffle M=1: break-even = P(win) = 1/N
    assert p_breakeven(1, 10) == pytest.approx(0.1, rel=0.01)

def test_strategy_score_peaks():
    # Score should peak around M=4N to 5N
    N = 10
    scores = {M: strategy_score(M, N) for M in range(1, 200)}
    peak_M = max(scores, key=scores.get)
    assert 20 <= peak_M <= 80

def test_win_pmf_sums_to_one():
    pmf = win_distribution_pmf(10, 10)
    total = sum(x["probability"] for x in pmf)
    assert total == pytest.approx(1.0, abs=0.01)

def test_first_win_pmf_sums_to_one():
    pmf = first_win_pmf(10, 10)
    total = sum(x["probability"] for x in pmf)
    assert total == pytest.approx(1.0, abs=0.01)
