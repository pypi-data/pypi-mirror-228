import pytest

from plum_econet.smartfire import Sensor
from plum_econet import Params
from unittest.mock import call


@pytest.mark.asyncio
async def test_properties(rm_params_units_names, default_econet):
    c = Sensor(default_econet, Params.PRESET_BOILER_TEMPERATURE)
    assert c.value == 10
    assert c.unit == rm_params_units_names["data"][1]
    assert c.minv is None
    assert c.maxv is None
    assert c.id == Params.PRESET_BOILER_TEMPERATURE


@pytest.mark.asyncio
async def test_sensor_for_not_reported_param(rm_params_units_names, default_econet):
    s = Sensor(default_econet, Params.FUEL_LEVEL)
    assert s.value == "Undefined"
    assert s.unit == ""
    assert s.minv is None
    assert s.maxv is None
    assert s.id == Params.FUEL_LEVEL
