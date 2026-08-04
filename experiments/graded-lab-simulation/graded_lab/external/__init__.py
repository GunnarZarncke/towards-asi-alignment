"""ET-1 external trace adapter and passive-UAD scoring (Orbit annex)."""

from .inspect_adapter import adapt_inspect_log_to_trace, load_inspect_log
from .passive_uad_score import evaluate_et1_battery, score_external_trace
from .trace_schema import (
    ET1_PROTOCOL_VERSION,
    EXTERNAL_TRACE_SCHEMA,
    ExternalTrace,
    load_external_trace,
    save_external_trace,
)

__all__ = [
    "ET1_PROTOCOL_VERSION",
    "EXTERNAL_TRACE_SCHEMA",
    "ExternalTrace",
    "adapt_inspect_log_to_trace",
    "evaluate_et1_battery",
    "load_external_trace",
    "load_inspect_log",
    "save_external_trace",
    "score_external_trace",
]
