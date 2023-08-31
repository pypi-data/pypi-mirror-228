#
# Copyright (c) 2023, Empa, Leonie Fierz, Aaron Bojarski, Ricardo Parreira da Silva, Sven Eggimann.
#
# This file is part of CESAR-P - Combined Energy Simulation And Retrofit written in Python
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Contact: https://www.empa.ch/web/s313
#
"""
results
============

Package for results processing.

This package does not include extracting the results from EnergyPlus, but uses for this the functions from :py:mod:`cesarp.eplus_adapter`
The package does not include calculating the operational emissions and costs, but uses for this :py:mod:`cesarp.emissions_cost`

=========================================================== ===========================================================
class                                                       description
=========================================================== ===========================================================
:py:class:`cesarp.results.ResultProcessor`                  Handling of annual results, including operational emissions and costs

=========================================================== ===========================================================
"""
