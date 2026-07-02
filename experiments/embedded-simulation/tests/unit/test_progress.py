from embedded_sim.progress import progress_interval


def test_progress_interval_explicit():
    assert progress_interval(1000, every=25) == 25


def test_progress_interval_auto():
    assert progress_interval(2310, every=0) == 23
    assert progress_interval(5, every=0) == 1
