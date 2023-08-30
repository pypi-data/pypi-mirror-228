import contextlib
from itertools import groupby
import json
import os
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from ddtrace import config
from ddtrace.internal import compat
from ddtrace.internal.logger import get_logger

from .constants import COVERAGE_TAG_NAME


log = get_logger(__name__)

try:
    from coverage import Coverage
    from coverage import version_info as coverage_version

    # this public attribute became private after coverage==6.3
    EXECUTE_ATTR = "_execute" if coverage_version > (6, 3) else "execute"
except ImportError:
    Coverage = None  # type: ignore[misc,assignment]
    EXECUTE_ATTR = ""


def enabled():
    if config._ci_visibility_code_coverage_enabled:
        if compat.PY2:
            return False
        if Coverage is None:
            log.warning(
                "CI Visibility code coverage tracking is enabled, but the `coverage` package is not installed. "
                "To use code coverage tracking, please install `coverage` from https://pypi.org/project/coverage/"
            )
            return False
        return True
    return False


@contextlib.contextmanager
def cover(span, root=None, **kwargs):
    """Calculates code coverage on the given span and saves it as a tag"""
    coverage_kwargs = {
        "data_file": None,
        "source": [root] if root else None,
        "config_file": False,
        "omit": [
            "*/site-packages/*",
        ],
    }
    coverage_kwargs.update(kwargs)
    cov = Coverage(**coverage_kwargs)
    cov.start()
    test_id = str(span.trace_id)
    cov.switch_context(test_id)
    yield cov
    cov.stop()
    span.set_tag(COVERAGE_TAG_NAME, build_payload(cov, test_id=test_id, root=root))


def segments(lines):
    # type: (Iterable[int]) -> List[Tuple[int, int, int, int, int]]
    """Extract the relevant report data for a single file."""
    _segments = []
    for key, g in groupby(enumerate(sorted(lines)), lambda x: x[1] - x[0]):
        group = list(g)
        start = group[0][1]
        end = group[-1][1]
        _segments.append((start, 0, end, 0, -1))

    return _segments


def _lines(coverage, context):
    # type: (Coverage, Optional[str]) -> Dict[str, List[Tuple[int, int, int, int, int]]]
    if not coverage._collector or not coverage._collector.data:
        return {}

    return {
        k: segments(v.keys()) if isinstance(v, dict) else segments(v)  # type: ignore
        for k, v in coverage._collector.data.items()
    }


def build_payload(coverage, test_id=None, root=None):
    # type: (Coverage, Optional[str], Optional[str]) -> str
    """
    Generate a CI Visibility coverage payload, formatted as follows:

    "files": [
        {
            "filename": <String>,
            "segments": [
                [Int, Int, Int, Int, Int],  # noqa
            ]
        },
        ...
    ]

    For each segment of code for which there is coverage, there are always five integer values:
        The first number indicates the start line of the code block (index starting in 1)
        The second number indicates the start column of the code block (index starting in 1). Use value -1 if the
            column is unknown.
        The third number indicates the end line of the code block
        The fourth number indicates the end column of the code block
        The fifth number indicates the number of executions of the block
            If the number is >0 then it indicates the number of executions
            If the number is -1 then it indicates that the number of executions are unknown

    :param test_id: a unique identifier for the current test run
    :param root: the directory relative to which paths to covered files should be resolved
    """
    return json.dumps(
        {
            "files": [
                {
                    "filename": os.path.relpath(filename, root) if root is not None else filename,
                    "segments": lines,
                }
                if lines
                else {
                    "filename": os.path.relpath(filename, root) if root is not None else filename,
                }
                for filename, lines in _lines(coverage, test_id).items()
            ]
        }
    )
