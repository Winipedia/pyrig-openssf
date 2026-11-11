"""Health check workflow extended with reusable security-practices analysis."""

from collections.abc import Callable
from typing import Any, override

from pyrig.rig.configs.version_control.remote.workflows.health_check import (
    HealthCheckWorkflowConfigFile as BaseHealthCheckWorkflowConfigFile,
)

from pyrig_openssf.rig.configs.version_control.remote.workflows.security_practices import (  # noqa: E501
    SecurityPracticesWorkflowConfigFile,
)


class HealthCheckWorkflowConfigFile(BaseHealthCheckWorkflowConfigFile):
    """Include security-practices checks in the required health-check result."""

    @override
    def jobs_health_check(self) -> tuple[Callable[[], dict[str, Any]], ...]:
        """Return base health-check jobs followed by security-practices analysis."""
        return (*super().jobs_health_check(), self.job_security_practices)

    def job_security_practices(self) -> dict[str, Any]:
        """Call the reusable security-practices workflow."""
        return self.job_workflow_call(
            self.job_security_practices,
            workflow=SecurityPracticesWorkflowConfigFile,
        )
