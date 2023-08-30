# -*- coding: utf-8 -*-
#
# Please refer to AUTHORS.rst for a complete list of Copyright holders.
# Copyright (C) 2016-2022, Agoras Developers.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import doctest
import unittest

from agoras.core.logger import logger


class TestLogger(unittest.TestCase):

    def setUp(self):
        logger.start()

    def test_01_default_level(self):
        pass


def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite('agoras.core.logger'))
    return tests


if __name__ == '__main__':
    sys.exit(unittest.main())
