"""Backports starting from Python 3.9"""
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
import re
import string
from typing import Any, List, Optional, Protocol, TypeVar

# pylint: disable=import-error
from . import PYMAJOR, PYMINOR, public
from .mixin import Mixin, mixin


class IsTemplatePre311(Protocol):
    """Protocol to check if a Template is pre-3.11"""

    delimiter: str
    idpattern: r'str'
    braceidpattern: r'Optional[str]'
    flags: int
    pattern: re.Pattern[str]
    template: str

    def safe_substitute(self: Any) -> Optional[str]:
        """Abstract method to be implemented by base"""

    def substitute(self: Any) -> Optional[str]:
        """Abstract method to be implemented by base"""


T = TypeVar('T', bound='string.Template')


class TemplateGetIdentifiersMixin(Mixin[Any]):
    """Example Template mixin with preferred way of typing and using mixins"""

    delimiter: str
    idpattern: r'str'
    braceidpattern: r'Optional[str]'
    flags: int
    pattern: re.Pattern[str]
    template: str

    def safe_substitute(self: object) -> Optional[str]:
        """Abstract method to be implemented by base"""

    def substitute(self: object) -> Optional[str]:
        """Abstract method to be implemented by base"""

    def get_identifiers(self: IsTemplatePre311) -> List[str]:  # pragma: defer to string
        """Mixin method get_identifiers for older Template pre-3.11"""
        ids = []
        for i in self.pattern.finditer(self.template):
            named = i.group('named') or i.group('braced')
            if named is not None and named not in ids:
                ids.append(named)
            elif named is None and i.group('invalid') is None and i.group('escaped') is None:
                raise ValueError('Unrecognized named group in pattern', self.pattern)
        return ids

    @classmethod
    def extend_with(cls: type[IsTemplatePre311], instance: T) -> T:
        """Extend the class with the mixin instance."""
        instance.__class__ = type(
            f'{instance.__class__.__name__}With{cls.__name__}',
            (instance.__class__, cls),
            {},
        )
        return instance


# pylint: disable=line-too-long
if PYMAJOR >= 3 and PYMINOR < 11:  # pragma: defer to python
    Template = public(
        mixin(TemplateGetIdentifiersMixin, string.Template)
    )  # pragma: defer to string
else:
    Template = public(string.Template)  # pragma: defer to string
