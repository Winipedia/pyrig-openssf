"""Explicit references for reviewed dead code false positives."""

from pyrig.rig.configs.base.workflow import WorkflowConfigFile

_CONFIG_FILE_OVERRIDES = (
    WorkflowConfigFile.jobs,
    WorkflowConfigFile.workflow_triggers,
)
