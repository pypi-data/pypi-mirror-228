# coding=utf-8
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
from dataclasses import dataclass
import pint


@dataclass
class TransparentMaterial:
    name: str
    back_side_infrared_hemispherical_emissivity: pint.Quantity
    back_side_solar_reflectance: pint.Quantity
    back_side_visible_reflectance: pint.Quantity
    conductivity: pint.Quantity
    dirt_correction_factor: pint.Quantity
    front_side_infrared_hemispherical_emissivity: pint.Quantity
    front_side_solar_reflectance: pint.Quantity
    front_side_visible_reflectance: pint.Quantity
    infrared_transmittance: pint.Quantity
    solar_transmittance: pint.Quantity
    visible_transmittance: pint.Quantity
    # Note for transparent material (used for window glass) there are no emission factors available, emission factors
    # are assigned for the whole window construction

    @property
    def short_name(self):
        if "/" in self.name:
            return str(self.name.rsplit("/", 1)[1])
        else:
            return self.name
