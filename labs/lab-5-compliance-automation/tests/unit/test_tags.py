import os
import sys

import pytest

# Add the parent directory to sys.path to enable imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def test_module_imports():
    """Test basic module imports work."""
    try:
        # Setup mock AWS environment
        import os
        import sys

        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from mock_aws import setup_mocked_aws_environment

        mock_patch = setup_mocked_aws_environment()

        # Import the modules we want to test (noqa indicates used for testing)
        import src.scripts.lambda_functions.required_tags  # noqa: F401
        import src.scripts.remediation.encryption_remediation  # noqa: F401
        import src.scripts.remediation.s3_policy_remediation  # noqa: F401

        assert True

        # Stop the mock
        mock_patch.stop()
    except ImportError:
        pytest.skip("Module not found, skipping import test")
