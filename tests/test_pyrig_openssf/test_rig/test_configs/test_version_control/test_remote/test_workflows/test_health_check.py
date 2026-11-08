"""Test module."""

from pyrig.rig.configs.version_control.remote.workflows.release import (
    ReleaseWorkflowConfigFile,
)

from pyrig_openssf.rig.configs.version_control.remote.workflows.health_check import (
    HealthCheckWorkflowConfigFile,
)
from pyrig_openssf.rig.configs.version_control.remote.workflows.scorecard import (
    ScorecardWorkflowConfigFile,
)


class TestHealthCheckWorkflowConfigFile:
    """Test class."""

    def test_job_scorecard(self) -> None:
        """Test method."""
        workflow = HealthCheckWorkflowConfigFile.I
        job = workflow.job_scorecard()
        assert job["job_id"] == "scorecard"
        assert job["uses"] == ScorecardWorkflowConfigFile.I.workflow_call_reference()
        assert job["permissions"] == workflow.job_scorecard_permissions()

    def test_job_scorecard_permissions(self) -> None:
        """Test method."""
        permissions = HealthCheckWorkflowConfigFile.I.job_scorecard_permissions()
        assert permissions == ScorecardWorkflowConfigFile.I.used_permissions()
        release_permissions = ReleaseWorkflowConfigFile.I.job_health_check_permissions()
        for name, level in permissions.items():
            assert release_permissions[name] == level

    def test_jobs_health_check(self) -> None:
        """Test method."""
        workflow = HealthCheckWorkflowConfigFile.I
        jobs = workflow.jobs_health_check()
        assert workflow.job_scorecard in jobs
