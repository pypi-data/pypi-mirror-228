from typing import Any
from typing import Dict
from typing import FrozenSet
from typing import Set
from typing import TYPE_CHECKING
from typing import Tuple

from ddtrace.contrib.trace_utils import set_flattened_tags


if TYPE_CHECKING:  # pragma: no cover
    from ddtrace.span import Span


EXCLUDED_ENDPOINT = frozenset({"kms", "sts", "sns", "kinesis", "events"})
EXCLUDED_ENDPOINT_TAGS = {
    "firehose": frozenset({"params.Records"}),
    "secretsmanager": frozenset({"params.SecretString", "params.SecretBinary"}),
}


def truncate_arg_value(value, max_len=1024):
    # type: (Any, int) -> Any
    """Truncate values which are bytes and greater than `max_len`.
    Useful for parameters like 'Body' in `put_object` operations.
    """
    if isinstance(value, bytes) and len(value) > max_len:
        return b"..."

    return value


def add_span_arg_tags(
    span,  # type: Span
    endpoint_name,  # type: str
    args,  # type: Tuple[Any]
    args_names,  # type: Tuple[str]
    args_traced,  # type: Set[str]
):
    # type: (...) -> None
    if endpoint_name not in EXCLUDED_ENDPOINT:
        exclude_set = EXCLUDED_ENDPOINT_TAGS.get(endpoint_name, frozenset())  # type: FrozenSet[str]
        set_flattened_tags(
            span,
            items=((name, value) for (name, value) in zip(args_names, args) if name in args_traced),
            exclude_policy=lambda tag: tag in exclude_set or tag.endswith("Body"),
            processor=truncate_arg_value,
        )


def _add_api_param_span_tags(span, endpoint_name, params):
    # type: (Span, str, Dict[str, Any]) -> None
    # Note: Only some boto3 requests will supply these params
    # i.e. that might explain why you see these tags being set to empty strings
    if endpoint_name == "cloudwatch":
        log_group_name = params.get("logGroupName")
        if log_group_name:
            span.set_tag_str("aws.cloudwatch.logs.log_group_name", log_group_name)
            span.set_tag_str("loggroupname", log_group_name)
    elif endpoint_name == "dynamodb":
        table_name = params.get("TableName")
        if table_name:
            span.set_tag_str("aws.dynamodb.table_name", table_name)
            span.set_tag_str("tablename", table_name)
    elif endpoint_name == "kinesis":
        stream_name = params.get("StreamName")
        if stream_name:
            span.set_tag_str("aws.kinesis.stream_name", stream_name)
            span.set_tag_str("streamname", stream_name)
    elif endpoint_name == "redshift":
        cluster_identifier = params.get("ClusterIdentifier")
        if cluster_identifier:
            span.set_tag_str("aws.redshift.cluster_identifier", cluster_identifier)
            span.set_tag_str("clusteridentifier", cluster_identifier)
    elif endpoint_name == "s3":
        bucket_name = params.get("Bucket")
        if bucket_name:
            span.set_tag_str("aws.s3.bucket_name", bucket_name)
            span.set_tag_str("bucketname", bucket_name)

    elif endpoint_name == "sns":
        topic_arn = params.get("TopicArn")
        if topic_arn:
            # example topicArn: arn:aws:sns:sa-east-1:1234:topicname
            span.set_tag_str("aws.sns.topic_arn", topic_arn)
            topicname = topic_arn.split(":")[-1]
            aws_account = topic_arn.split(":")[-2]
            span.set_tag_str("aws_account", aws_account)
            span.set_tag_str("topicname", topicname)

    elif endpoint_name == "sqs":
        queue_name = params.get("QueueName", "")
        queue_url = params.get("QueueUrl")
        if queue_url and (queue_url.startswith("sqs:") or queue_url.startswith("http")):
            # example queue_url: https://sqs.sa-east-1.amazonaws.com/12345678/queuename
            queue_name = queue_url.split("/")[-1]
            aws_account = queue_url.split("/")[-2]
            span.set_tag_str("aws_account", aws_account)
        span.set_tag_str("aws.sqs.queue_name", queue_name)
        span.set_tag_str("queuename", queue_name)

    elif endpoint_name == "lambda":
        function_name = params.get("FunctionName", "")
        span.set_tag_str("functionname", function_name)

    elif endpoint_name == "events":
        rule_name = params.get("Name", "")
        span.set_tag_str("rulename", rule_name)

    elif endpoint_name == "states":
        state_machine_arn = params.get("stateMachineArn", "")
        span.set_tag_str("statemachinearn", state_machine_arn)


AWSREGION = "aws.region"
REGION = "region"
AGENT = "aws.agent"
OPERATION = "aws.operation"
