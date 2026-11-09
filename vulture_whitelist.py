"""Explicit references for reviewed dead code false positives."""

from pyrig.rig.configs.base.config_file import ConfigFile
from pyrig.rig.configs.base.workflow import WorkflowConfigFile
from pyrig.rig.tools.base.tool import Tool

_CONFIG_FILE_OVERRIDES = (
    ConfigFile.stem,
    WorkflowConfigFile.jobs,
    WorkflowConfigFile.workflow_triggers,
)
_TOOL_OVERRIDES = (
    Tool.dev_dependencies,
    Tool.group,
    Tool.image_url,
    Tool.link_url,
)
