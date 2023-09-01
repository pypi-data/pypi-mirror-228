import pytest
import re

from plum_econet import Params, Econet
from plum_econet.exceptions import EconetHTTPException, EconetUnauthorized


@pytest.mark.asyncio
async def test_econet_setup(
    rm_params_enums,
    rm_params_units_names,
    rm_alarms_names,
    rm_current_data_params,
    rm_params_data,
    reg_params_data,
    sys_params,
):
    econet = Econet("http://localhost", "user", "pass")
    await econet.setup()
    assert econet.enums == rm_params_enums["data"]
    assert econet.units == rm_params_units_names["data"]
    assert len(econet.params) == 2
    param1 = econet.get_param(Params.PRESET_BOILER_TEMPERATURE)
    assert param1.special == 1
    assert param1.unit == econet.units[1]
    assert param1.edit is False
    assert param1.minv is None
    assert param1.maxv is None
    assert param1.mult is None
    assert param1.offset is None
    assert param1.desc == "Test PRESET_BOILER_TEMPERATURE"
    assert param1.value == 10

    param2 = econet.get_param(Params.EDIT_PRESET_BOILER_TEMPERATURE)
    assert param2.special is None
    assert param2.unit == econet.units[1]
    assert param2.edit is True
    assert param2.minv == 15
    assert param2.maxv == 25
    assert param2.mult == 1.0
    assert param2.offset == 0
    assert param2.desc == ""
    assert param2.value == 20


@pytest.mark.asyncio
async def test_econet_update(
    rm_params_enums,
    rm_params_units_names,
    rm_alarms_names,
    rm_current_data_params,
    rm_params_data,
    reg_params_data,
    sys_params,
):
    econet = Econet("http://localhost", "user", "pass")
    await econet.setup()
    param1 = econet.get_param(Params.PRESET_BOILER_TEMPERATURE)
    assert param1.special == 1
    assert param1.unit == econet.units[1]
    assert param1.edit is False
    assert param1.minv is None
    assert param1.maxv is None
    assert param1.mult is None
    assert param1.offset is None
    assert param1.desc == "Test PRESET_BOILER_TEMPERATURE"
    param2 = econet.get_param(Params.EDIT_PRESET_BOILER_TEMPERATURE)
    assert param2.special is None
    assert param2.unit == econet.units[1]
    assert param2.edit is True
    assert param2.minv == 15
    assert param2.maxv == 25
    assert param2.mult == 1.0
    assert param2.offset == 0
    assert param2.desc == ""
    assert param2.value == 20
    await econet.update()
    assert param1.value == 10
    assert param2.value == 20


@pytest.mark.asyncio
async def test_econet_setup_auth_error(aioresponses):
    pattern = re.compile(r"^http://localhost/econet/.*$")
    aioresponses.get(pattern, status=401)
    econet = Econet("http://localhost", "user", "pass")
    with pytest.raises(EconetUnauthorized):
        await econet.setup()


@pytest.mark.asyncio
async def test_econet_setup_http_error(aioresponses):
    pattern = re.compile(r"^http://localhost/econet/.*$")
    aioresponses.get(pattern, status=502)
    econet = Econet("http://localhost", "user", "pass")
    with pytest.raises(EconetHTTPException) as exc:
        await econet.setup()
    assert str(exc.value).startswith(
        "Got 502 Bad Gateway when calling http://localhost/econet/"
    )


@pytest.mark.asyncio
async def test_not_reported_param(rm_params_units_names, default_econet):
    """It may happen, that given paramter won't be returned in responses from the API.
    One such parameter is FUEL_LEVEL, which is not visible in responses from API if
    Fuel Level was not callibrated in the Smartfire furnace."""
    param = default_econet.get_param(Params.FUEL_LEVEL)
    assert param.value == "Undefined"
    assert param.unit == ""
    assert param.minv is None
    assert param.maxv is None
    assert param.id == Params.FUEL_LEVEL


@pytest.mark.asyncio
async def test_not_reported_param_with_reported_data(
    rm_params_units_names, default_econet, aioresponses
):
    param = default_econet.get_param(Params.FUEL_LEVEL)
    assert param.value == "Undefined"
    assert param.unit == ""
    assert param.minv is None
    assert param.maxv is None
    assert param.id == Params.FUEL_LEVEL
    payload = {"data": {"1280": 10, Params.FUEL_LEVEL.value: 99}}
    aioresponses.get("http://localhost/econet/regParamsData", payload=payload)
    await default_econet.update()
    assert Params.FUEL_LEVEL.value not in default_econet.params
