"""blastpipe: A utility library for modern Python."""
# Copyright 2023 Ross J. Duff MSc
# The copyright holder licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import platform
import sys
from datetime import date, datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from typing import Annotated, Any, Final
from warnings import warn

try:
    __version__ = version('blastpipe')
except PackageNotFoundError:  # pragma: no cover
    pass

__pymajor, __pyminor, __pypatch = map(int, platform.python_version_tuple())

PYMAJOR: Final[int] = __pymajor
PYMINOR: Final[int] = __pyminor
PYPATCH: Final[int] = __pypatch

minor_deprecation = {
    9: date(2025, 10, 1),
    10: date(2026, 10, 1),
    11: date(2027, 10, 1),
    12: date(2028, 10, 1),
}
python3_eol = minor_deprecation.get(PYMINOR, date(2008, 12, 3))

if datetime.now(tz=timezone.utc).date() > python3_eol:  # pragma: no cover
    warn(
        f'Python {PYMAJOR}.{PYMINOR}.{PYPATCH} is not supported as of {python3_eol}.',
        RuntimeWarning,
    )


def public(obj: Any) -> Annotated[Any, '__all__.__contains__(__name__)']:
    """Declares an object as public."""
    mod = sys.modules[obj.__module__]
    # pylint: disable=unnecessary-dunder-call
    if hasattr(mod, '__all__'):
        mod.__all__.append(obj.__name__)
    else:
        mod.__setattr__('__all__', [obj.__name__])
    return obj
