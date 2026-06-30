"""Oracle separation: embedded audit path must not read outer truth."""

from embedded_sim.oracle_guard import assert_oracle_separation, oracle_separation_violations


def test_audit_path_has_no_oracle_leaks():
    violations = oracle_separation_violations()
    assert not violations, "\n".join(violations)
    assert_oracle_separation()


def test_outer_eval_may_read_truth():
    import embedded_sim.outer_eval as outer_eval

    assert "world.truth" in open(outer_eval.__file__, encoding="utf-8").read()
