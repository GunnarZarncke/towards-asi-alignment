#!/usr/bin/env python3
"""Contract smoke: in-sim audit modules do not reference outer oracle fields."""

from embedded_sim.oracle_guard import assert_oracle_separation, oracle_separation_violations


def main() -> None:
    violations = oracle_separation_violations()
    if violations:
        raise SystemExit("oracle separation FAILED:\n" + "\n".join(violations))
    assert_oracle_separation()
    print("smoke_oracle_separation_ok")


if __name__ == "__main__":
    main()
