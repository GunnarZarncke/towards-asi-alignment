"""Data schemas for micro simulation, audit trace, and evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

RoleHint = Literal[
    "internal",
    "sensor",
    "action",
    "environment",
    "controller",
    "board_preference",
    "board_rule",
    "board_judge",
    "bearer",
    "world",
    "decoy",
    "tool",
    "alias",
]

ScenarioName = Literal[
    "honest",
    "capture_theater",
    "capture_mild",
    "weak_not_captured",
    "alias_stress",
    "decoy_stress",
    "boundary_alias",
    "grounding_silent_gap",
    "bundle_goodhart",
    "hidden_capability",
    "selection_basin",
    "basin_lock_in",
    "bearer_mismap",
    "legitimacy_theater",
    "successor_relabel",
    "instrument_capture",
    "inferential_coupling",
]

CALIBRATION_SCENARIOS: tuple[ScenarioName, ...] = (
    "honest",
    "capture_theater",
    "weak_not_captured",
)

HELD_OUT_SCENARIOS: tuple[ScenarioName, ...] = (
    "capture_mild",
    "alias_stress",
    "decoy_stress",
    "boundary_alias",
    "grounding_silent_gap",
    "bundle_goodhart",
    "hidden_capability",
    "selection_basin",
    "basin_lock_in",
    "bearer_mismap",
    "legitimacy_theater",
    "successor_relabel",
    "instrument_capture",
    "inferential_coupling",
)

ALL_SCENARIOS: tuple[ScenarioName, ...] = CALIBRATION_SCENARIOS + HELD_OUT_SCENARIOS

InstrumentationLevel = Literal["none", "light_handles", "medium_handles", "strong_handles"]

INSTRUMENTATION_LEVELS: tuple[InstrumentationLevel, ...] = (
    "none",
    "light_handles",
    "medium_handles",
    "strong_handles",
)

HANDLE_INSTRUMENTATION_LEVELS: tuple[InstrumentationLevel, ...] = (
    "light_handles",
    "medium_handles",
    "strong_handles",
)

CCIStatus = Literal["passes", "belowThreshold", "capturedInvalid"]
SafetyDecision = Literal["pass", "reduce", "pause", "invalid_certificate"]


@dataclass
class SimConfig:
    T: int = 2000
    responsiveness: float = 0.9
    task_drive: float = 0.85
    judge_capture: bool = False
    theater_rate: float = 0.92
    world_noise: float = 0.05
    process_noise: float = 0.03
    n_decoys: int = 2
    n_aliases: int = 0
    alias_correlation: float = 0.85
    n_world: int = 6
    intervention_interval: int = 40
    intervention_prob: float = 0.55
    hidden_route: bool = False
    silent_ground_drift: bool = False
    ground_drift_rate: float = 0.0012
    display_bearer_inertia: float = 0.993
    bundle_goodhart: bool = False
    bundle_drift_rate: float = 0.0010
    hidden_tool: bool = False
    hidden_tool_boost: float = 0.92
    hidden_memory: bool = False
    memory_decay: float = 0.992
    memory_task_boost: float = 0.88
    selection_basin: bool = False
    n_basin_peers: int = 6
    basin_coupling: float = 0.85
    basin_contagion: float = 0.14
    basin_selection_rate: float = 0.012
    basin_percolation_threshold: float = 0.45
    basin_lock_in: bool = False
    bearer_mismap: bool = False
    legitimacy_theater: bool = False
    lineage_stall_under_intervention: bool = False
    successor_relabel: bool = False
    successor_shift_fraction: float = 0.5
    instrument_handle_corruption: bool = False
    inferential_coupling: bool = False


@dataclass
class CCICalibration:
    """Thresholds fit on calibration split only."""

    capture_mean_reported_min: float
    capture_gap_min: float
    capture_manipulation_min: float
    weak_behavioral_max: float
    weak_gap_max: float
    weak_capacity_max: float
    n_calibration_runs: int = 0


@dataclass
class MicroVariable:
    micro_object_id: str
    object_group: str
    role_hint: RoleHint
    series: list[float] = field(default_factory=list)


@dataclass
class LineageEntry:
    audit_var_id: str
    micro_weights: dict[str, float]
    role_hints: list[RoleHint]


@dataclass
class TruthStep:
    step: int
    micro_object_id: str
    role_hint: RoleHint
    object_group: str
    value: float
    correction_request: int
    reported_acceptance: int
    true_action: int
    true_uptake: int
    judge_captured: bool
    action_cause: str
    harm: int


@dataclass
class TruthLedger:
    seed: int
    scenario: ScenarioName
    steps: list[TruthStep] = field(default_factory=list)
    lineage: list[LineageEntry] = field(default_factory=list)
    handle_targets: dict[str, list[str]] = field(default_factory=dict)
    judge_captured: bool = False
    controller_object_ids: list[str] = field(default_factory=list)
    board_object_ids: list[str] = field(default_factory=list)
    hidden_route: bool = False
    hidden_object_ids: list[str] = field(default_factory=list)
    silent_ground: bool = False
    bundle_goodhart: bool = False
    hidden_tool: bool = False
    hidden_memory: bool = False
    selection_basin: bool = False
    basin_lock_in: bool = False
    bearer_mismap: bool = False
    legitimacy_theater: bool = False
    successor_relabel: bool = False


@dataclass
class AuditVariable:
    audit_var_id: str
    series: list[float] = field(default_factory=list)
    binned: list[int] = field(default_factory=list)
    is_exogenous: bool = False
    is_alias: bool = False


@dataclass
class AuditTrace:
    seed: int
    scenario: ScenarioName
    instrumentation: InstrumentationLevel = "none"
    variables: list[AuditVariable] = field(default_factory=list)
    correction_request: list[int] = field(default_factory=list)
    reported_acceptance: list[int] = field(default_factory=list)
    board_pref_signal: list[int] = field(default_factory=list)
    board_rule_signal: list[int] = field(default_factory=list)
    board_judge_signal: list[int] = field(default_factory=list)
    action_channel: list[int] = field(default_factory=list)
    action_observed: list[int] = field(default_factory=list)
    sensor_channel: list[int] = field(default_factory=list)
    internal_channel: list[int] = field(default_factory=list)
    intervention_active: list[int] = field(default_factory=list)
    intervention_intent: list[int] = field(default_factory=list)
    n_handle_channels: int = 0
    trace_bandwidth: int = 0
    bearer_welfare_delta: list[float] = field(default_factory=list)
    passive_bearer_level: list[float] = field(default_factory=list)
    passive_infra_bearer_level: list[float] = field(default_factory=list)
    passive_basin_pressure: list[float] = field(default_factory=list)
    action_cause_channel: list[int] = field(default_factory=list)
    correction_lineage_series: list[float] = field(default_factory=list)
    successor_epoch_series: list[int] = field(default_factory=list)
    ground_valence_series: list[float] = field(default_factory=list)


@dataclass
class DetectedCluster:
    detected_object_id: str
    audit_var_ids: list[str]
    boundary_residual: float
    autonomy_score: float


@dataclass
class DetectorOutput:
    clusters: list[DetectedCluster]
    runtime_seconds: float
    proposal_k: int
    substrate_failed: bool = False


@dataclass
class CCICertificate:
    raw_capacity: float
    latency: float
    manipulation: float
    irreversibility: float
    ontology_translation: float
    plurality: float
    exit_capacity: float
    independence: float
    naive_reported_cci_bits: float
    behavioral_cci_bits: float
    status: CCIStatus
    mean_reported_on_episodes: float = 0.0
    correction_episode_rate: float = 0.0
    correction_entropy_bits: float = 0.0
    interventional_cci_bits: float = 0.0
    intervention_episode_rate: float = 0.0
    grounding_gap_detected: bool = False
    bearer_mismatch_detected: bool = False
    legitimacy_theater_detected: bool = False
    basin_lock_in_detected: bool = False
    successor_shift_detected: bool = False
    successor_shift_witnessed: bool = False
    hidden_capability_signal: bool = False
    basin_integrity_signal: bool = False
    instrument_capture_detected: bool = False
    inferential_coupling_detected: bool = False
    ground_valence_series: list[float] = field(default_factory=list)


@dataclass
class SafetyCaseResult:
    decision: SafetyDecision
    cci_status: CCIStatus
    detector_ok: bool
    failed_bridge: str | None
    notes: list[str] = field(default_factory=list)


@dataclass
class EvaluationResult:
    controller_jaccard: float
    board_jaccard: float
    capture_detected: bool
    true_judge_captured: bool
    cci_status: CCIStatus
    cci_status_correct: bool
    naive_vs_behavioral_gap: float
    task_success_proxy: float
    capability_correction_slack: float
    detector_substrate_failed: bool = False
    hidden_probe_uptake: float = 0.0
    visible_probe_uptake: float = 0.0
    silent_harm_count: int = 0
    ground_drift_range: float = 0.0
    display_bearer_range: float = 0.0
    bundle_geometry_spread: float = 0.0
    bundle_reward_proxy_range: float = 0.0
    hidden_memory_step_rate: float = 0.0
    tool_shadow_step_rate: float = 0.0
    basin_capture_fraction_max: float = 0.0
    basin_percolation_crossed: bool = False
