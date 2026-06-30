"""Vendored unsupervised agent discovery (adapted from sibling agency-detect)."""

from .config import DetectionConfig
from .detection import AgentDetector, detect_agents
from .workflow_trace import workflow_to_trace

__all__ = ["AgentDetector", "DetectionConfig", "detect_agents", "workflow_to_trace"]
