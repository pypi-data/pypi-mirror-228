from os import environ
from os import path


def in_aws_lambda():
    # type: () -> bool
    """Returns whether the environment is an AWS Lambda.
    This is accomplished by checking if the AWS_LAMBDA_FUNCTION_NAME environment
    variable is defined.
    """
    return bool(environ.get("AWS_LAMBDA_FUNCTION_NAME", False))


def has_aws_lambda_agent_extension():
    # type: () -> bool
    """Returns whether the environment has the AWS Lambda Datadog Agent
    extension available.
    """
    return path.exists("/opt/extensions/datadog-agent")


def in_gcp_function():
    # type: () -> bool
    """Returns whether the environment is a GCP Function.
    This is accomplished by checking for the presence of one of two pairs of environment variables,
    with one pair being set by deprecated GCP Function runtimes, and the other set by newer runtimes.
    """
    is_deprecated_gcp_function = environ.get("FUNCTION_NAME", "") != "" and environ.get("GCP_PROJECT", "") != ""
    is_newer_gcp_function = environ.get("K_SERVICE", "") != "" and environ.get("FUNCTION_TARGET", "") != ""
    return is_deprecated_gcp_function or is_newer_gcp_function
