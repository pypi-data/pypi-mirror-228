"""
Trace queries along a session to a cassandra cluster
"""
import sys


try:
    import cassandra.cluster as cassandra_cluster
except AttributeError:
    from cassandra import cluster as cassandra_cluster

from ddtrace import config
from ddtrace.internal.constants import COMPONENT

from ...constants import ANALYTICS_SAMPLE_RATE_KEY
from ...constants import ERROR_MSG
from ...constants import ERROR_TYPE
from ...constants import SPAN_KIND
from ...constants import SPAN_MEASURED_KEY
from ...ext import SpanKind
from ...ext import SpanTypes
from ...ext import cassandra as cassx
from ...ext import db
from ...ext import net
from ...internal.compat import maybe_stringify
from ...internal.compat import stringify
from ...internal.logger import get_logger
from ...internal.schema import schematize_database_operation
from ...internal.schema import schematize_service_name
from ...internal.utils import get_argument_value
from ...internal.utils.formats import deep_getattr
from ...pin import Pin
from ...vendor import wrapt


log = get_logger(__name__)

RESOURCE_MAX_LENGTH = 5000
SERVICE = schematize_service_name("cassandra")
CURRENT_SPAN = "_ddtrace_current_span"
PAGE_NUMBER = "_ddtrace_page_number"


# Original connect connect function
_connect = cassandra_cluster.Cluster.connect


def patch():
    """patch will add tracing to the cassandra library."""
    setattr(cassandra_cluster.Cluster, "connect", wrapt.FunctionWrapper(_connect, traced_connect))
    Pin(service=SERVICE).onto(cassandra_cluster.Cluster)


def unpatch():
    cassandra_cluster.Cluster.connect = _connect


def traced_connect(func, instance, args, kwargs):
    session = func(*args, **kwargs)
    if not isinstance(session.execute, wrapt.FunctionWrapper):
        # FIXME[matt] this should probably be private.
        setattr(session, "execute_async", wrapt.FunctionWrapper(session.execute_async, traced_execute_async))
    return session


def _close_span_on_success(result, future):
    span = getattr(future, CURRENT_SPAN, None)
    if not span:
        log.debug("traced_set_final_result was not able to get the current span from the ResponseFuture")
        return
    try:
        span.set_tags(_extract_result_metas(cassandra_cluster.ResultSet(future, result)))
    except Exception:
        log.debug("an exception occurred while setting tags", exc_info=True)
    finally:
        span.finish()
        delattr(future, CURRENT_SPAN)


def traced_set_final_result(func, instance, args, kwargs):
    result = get_argument_value(args, kwargs, 0, "response")
    _close_span_on_success(result, instance)
    return func(*args, **kwargs)


def _close_span_on_error(exc, future):
    span = getattr(future, CURRENT_SPAN, None)
    if not span:
        log.debug("traced_set_final_exception was not able to get the current span from the ResponseFuture")
        return
    try:
        # handling the exception manually because we
        # don't have an ongoing exception here
        span.error = 1
        span.set_tag_str(ERROR_MSG, exc.args[0])
        span.set_tag_str(ERROR_TYPE, exc.__class__.__name__)
    except Exception:
        log.debug("traced_set_final_exception was not able to set the error, failed with error", exc_info=True)
    finally:
        span.finish()
        delattr(future, CURRENT_SPAN)


def traced_set_final_exception(func, instance, args, kwargs):
    exc = get_argument_value(args, kwargs, 0, "response")
    _close_span_on_error(exc, instance)
    return func(*args, **kwargs)


def traced_start_fetching_next_page(func, instance, args, kwargs):
    has_more_pages = getattr(instance, "has_more_pages", True)
    if not has_more_pages:
        return func(*args, **kwargs)
    session = getattr(instance, "session", None)
    cluster = getattr(session, "cluster", None)
    pin = Pin.get_from(cluster)
    if not pin or not pin.enabled():
        return func(*args, **kwargs)

    # In case the current span is not finished we make sure to finish it
    old_span = getattr(instance, CURRENT_SPAN, None)
    if old_span:
        log.debug("previous span was not finished before fetching next page")
        old_span.finish()

    query = getattr(instance, "query", None)

    span = _start_span_and_set_tags(pin, query, session, cluster)

    page_number = getattr(instance, PAGE_NUMBER, 1) + 1
    setattr(instance, PAGE_NUMBER, page_number)
    setattr(instance, CURRENT_SPAN, span)
    try:
        return func(*args, **kwargs)
    except Exception:
        with span:
            span.set_exc_info(*sys.exc_info())
        raise


def traced_execute_async(func, instance, args, kwargs):
    cluster = getattr(instance, "cluster", None)
    pin = Pin.get_from(cluster)
    if not pin or not pin.enabled():
        return func(*args, **kwargs)

    query = get_argument_value(args, kwargs, 0, "query")

    span = _start_span_and_set_tags(pin, query, instance, cluster)

    try:
        result = func(*args, **kwargs)
        setattr(result, CURRENT_SPAN, span)
        setattr(result, PAGE_NUMBER, 1)
        setattr(result, "_set_final_result", wrapt.FunctionWrapper(result._set_final_result, traced_set_final_result))
        setattr(
            result,
            "_set_final_exception",
            wrapt.FunctionWrapper(result._set_final_exception, traced_set_final_exception),
        )
        setattr(
            result,
            "start_fetching_next_page",
            wrapt.FunctionWrapper(result.start_fetching_next_page, traced_start_fetching_next_page),
        )
        # Since we cannot be sure that the previous methods were overwritten
        # before the call ended, we add callbacks that will be run
        # synchronously if the call already returned and we remove them right
        # after.
        result.add_callbacks(
            _close_span_on_success, _close_span_on_error, callback_args=(result,), errback_args=(result,)
        )
        result.clear_callbacks()
        return result
    except Exception:
        with span:
            span.set_exc_info(*sys.exc_info())
        raise


def _start_span_and_set_tags(pin, query, session, cluster):
    service = pin.service
    tracer = pin.tracer
    span_name = schematize_database_operation("cassandra.query", database_provider="cassandra")
    span = tracer.trace(span_name, service=service, span_type=SpanTypes.CASSANDRA)

    span.set_tag_str(COMPONENT, config.cassandra.integration_name)
    span.set_tag_str(db.SYSTEM, "cassandra")

    # set span.kind to the type of request being performed
    span.set_tag_str(SPAN_KIND, SpanKind.CLIENT)

    span.set_tag(SPAN_MEASURED_KEY)
    _sanitize_query(span, query)
    span.set_tags(_extract_session_metas(session))  # FIXME[matt] do once?
    span.set_tags(_extract_cluster_metas(cluster))
    # set analytics sample rate if enabled
    span.set_tag(ANALYTICS_SAMPLE_RATE_KEY, config.cassandra.get_analytics_sample_rate())
    return span


def _extract_session_metas(session):
    metas = {}

    if getattr(session, "keyspace", None):
        # FIXME the keyspace can be overridden explicitly in the query itself
        # e.g. 'select * from trace.hash_to_resource'
        metas[cassx.KEYSPACE] = session.keyspace.lower()

    return metas


def _extract_cluster_metas(cluster):
    metas = {}
    if deep_getattr(cluster, "metadata.cluster_name"):
        metas[cassx.CLUSTER] = cluster.metadata.cluster_name
    if getattr(cluster, "port", None):
        metas[net.TARGET_PORT] = cluster.port

    return metas


def _extract_result_metas(result):
    metas = {}
    if result is None:
        return metas

    future = getattr(result, "response_future", None)

    if future:
        # get the host
        host = maybe_stringify(getattr(future, "coordinator_host", None))
        if host:
            host, _, port = host.partition(":")
            metas[net.TARGET_HOST] = host
            if port:
                metas[net.TARGET_PORT] = int(port)
        elif hasattr(future, "_current_host"):
            address = deep_getattr(future, "_current_host.address")
            if address:
                metas[net.TARGET_HOST] = address

        query = getattr(future, "query", None)
        if getattr(query, "consistency_level", None):
            metas[cassx.CONSISTENCY_LEVEL] = query.consistency_level
        if getattr(query, "keyspace", None):
            metas[cassx.KEYSPACE] = query.keyspace.lower()

        page_number = getattr(future, PAGE_NUMBER, 1)
        has_more_pages = getattr(future, "has_more_pages")
        is_paginated = has_more_pages or page_number > 1
        metas[cassx.PAGINATED] = is_paginated
        if is_paginated:
            metas[cassx.PAGE_NUMBER] = page_number

    if hasattr(result, "current_rows"):
        result_rows = result.current_rows or []
        metas[db.ROWCOUNT] = len(result_rows)

    return metas


def _sanitize_query(span, query):
    # TODO (aaditya): fix this hacky type check. we need it to avoid circular imports
    t = type(query).__name__

    resource = None
    if t in ("SimpleStatement", "PreparedStatement"):
        # reset query if a string is available
        resource = getattr(query, "query_string", query)
    elif t == "BatchStatement":
        resource = "BatchStatement"
        # Each element in `_statements_and_parameters` is:
        #   (is_prepared, statement, parameters)
        #  ref:https://github.com/datastax/python-driver/blob/13d6d72be74f40fcef5ec0f2b3e98538b3b87459/cassandra/query.py#L844
        #
        # For prepared statements, the `statement` value is just the query_id
        #   which is not a statement and when trying to join with other strings
        #   raises an error in python3 around joining bytes to unicode, so this
        #   just filters out prepared statements from this tag value
        q = "; ".join(q[1] for q in query._statements_and_parameters[:2] if not q[0])
        span.set_tag_str("cassandra.query", q)
        span.set_metric("cassandra.batch_size", len(query._statements_and_parameters))
    elif t == "BoundStatement":
        ps = getattr(query, "prepared_statement", None)
        if ps:
            resource = getattr(ps, "query_string", None)
    elif t == "str":
        resource = query
    else:
        resource = "unknown-query-type"  # FIXME[matt] what else do to here?

    span.resource = stringify(resource)[:RESOURCE_MAX_LENGTH]
