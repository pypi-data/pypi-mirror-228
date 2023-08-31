# Copyright 2016 Enzo Busseti, Stephen Boyd, Steven Diamond, BlackRock Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class DataError(Exception):
    """Base class for exception related to data."""

    pass


class MissingValuesError(DataError):
    """Cvxportfolio tried to access numpy.nan values."""

    pass


class ForeCastError(DataError):
    """Forecast procedure failed."""
    pass


class PortfolioOptimizationError(Exception):
    """Errors with portfolio optimization problems."""
