"""Health check workflow extended with reusable Scorecard analysis."""

from collections.abc import Callable
from typing import Any, override

from pyrig.rig.configs.version_control.remote.workflows.health_check import (
    HealthCheckWorkflowConfigFile as BaseHealthCheckWorkflowConfigFile,
)

from pyrig_openssf.rig.configs.version_control.remote.workflows.scorecard import (
    ScorecardWorkflowConfigFile,
)


class HealthCheckWorkflowConfigFile(BaseHealthCheckWorkflowConfigFile):
    """Include Scorecard in the required health check result."""

    @override
    def jobs_health_check(self) -> tuple[Callable[[], dict[str, Any]], ...]:
        """Return the base health-check job builders followed by the Scorecard call."""
        return (*super().jobs_health_check(), self.job_scorecard)

    def job_scorecard(self) -> dict[str, Any]:
        """Call the reusable Scorecard workflow."""
        return self.job(
            self.job_scorecard,
            uses=ScorecardWorkflowConfigFile.I.workflow_call_reference(),
            permissions=self.job_scorecard_permissions(),
            secrets=ScorecardWorkflowConfigFile.I.used_secrets_mapping() or None,
        )

    def job_scorecard_permissions(self) -> dict[str, Any]:
        """Return the permissions required by the Scorecard workflow."""
        return ScorecardWorkflowConfigFile.I.used_permissions()
