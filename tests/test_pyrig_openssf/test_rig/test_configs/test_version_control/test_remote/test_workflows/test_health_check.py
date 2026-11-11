"""Test module."""

from pyrig_openssf.rig.configs.version_control.remote.workflows.health_check import (
    HealthCheckWorkflowConfigFile,
)
from pyrig_openssf.rig.configs.version_control.remote.workflows.security_practices import (  # noqa: E501
    SecurityPracticesWorkflowConfigFile,
)


class TestHealthCheckWorkflowConfigFile:
    """Test class."""

    def test_job_security_practices(self) -> None:
        """Test method."""
        workflow = HealthCheckWorkflowConfigFile.I
        job = workflow.job_security_practices()
        assert job["job_id"] == "security-practices"
        assert (
            job["uses"]
            == SecurityPracticesWorkflowConfigFile.I.workflow_call_reference()
        )
        assert job["permissions"] == (
            SecurityPracticesWorkflowConfigFile.I.used_permissions()
        )
        assert job.get("secrets") == (
            SecurityPracticesWorkflowConfigFile.I.used_secrets_mapping() or None
        )

    def test_jobs_health_check(self) -> None:
        """Test method."""
        workflow = HealthCheckWorkflowConfigFile.I
        jobs = workflow.jobs_health_check()
        assert workflow.job_security_practices in jobs
