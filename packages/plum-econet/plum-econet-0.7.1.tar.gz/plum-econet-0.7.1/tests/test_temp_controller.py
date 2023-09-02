import pytest

from plum_econet.smartfire import TempController
from plum_econet import Params
from unittest.mock import call


@pytest.mark.asyncio
async def test_properties(sys_params, default_econet):
    c = TempController(
        default_econet,
        Params.PRESET_BOILER_TEMPERATURE,
        Params.EDIT_PRESET_BOILER_TEMPERATURE,
    )
    assert c.temperature == 10
    assert c.target_temperature == 20
    assert c.target_temperature_min == 15
    assert c.target_temperature_max == 25
    for temp in [24, 16, 25, 15]:
        await c.set_target_temperature(temp)
        default_econet.set_param.assert_has_calls(
            [call(Params.EDIT_PRESET_BOILER_TEMPERATURE.value, temp)]
        )
    with pytest.raises(ValueError):
        await c.set_target_temperature(26)
    with pytest.raises(ValueError):
        await c.set_target_temperature(14)
