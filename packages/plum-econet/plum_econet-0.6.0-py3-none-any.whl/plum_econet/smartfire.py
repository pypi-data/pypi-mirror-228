import asyncio
from .params import Params
from .econet import Econet
from .exceptions import EconetUninitilized


class Sensor(object):
    """
    Simple piece of information.
    """

    def __init__(self, econet: Econet, param_id: Params):
        self._param_name = param_id._name_
        self._param = econet.get_param(param_id)
        self._econet = econet

    def __str__(self):
        return f"{str(self.value)}{str(self.unit)}"

    def __repr__(self):
        return (
            f"{repr(self.__class__.__name__)}"
            f"(econet={repr(self._econet)}, param_id={repr(self._param.id)})"
        )

    @property
    def value(self) -> int | str:
        return self._param.value

    @property
    def id(self) -> int | str:
        return self._param.id

    @property
    def unit(self) -> str:
        return self._param.unit

    @property
    def minv(self) -> int:
        return self._param.minv

    @property
    def maxv(self) -> int:
        return self._param.maxv


class Setting(Sensor):
    """
    Represents single setting of the Econet device
    """

    async def set_value(self, value: int) -> int:
        if self.minv is not None and self.maxv is not None:
            if value < self.minv or value > self.maxv:
                raise ValueError(
                    f"Value {value} not in boundries <{self.minv},{self.maxv}>"
                    f" for Setting {self._param_name}"
                )

        task = asyncio.create_task(self._econet.set_param(self._param.id.value, value))
        await task
        return self.value


class TempController(object):
    """
    Class that controlls one aspect of a furnace, for example boiler temperature or huw temperature.
    """

    def __init__(
        self, econet: Econet, current_temp: Params, target_temp: Params
    ) -> None:
        self._econet = econet
        self._current_temp = Sensor(econet, current_temp)
        self._target_temp = Setting(econet, target_temp)

    @property
    def temperature(self) -> int:
        """Current temeperature."""
        return self._current_temp.value

    @property
    def target_temperature(self) -> int:
        """Current preset value for temperature."""
        return self._target_temp.value

    async def set_target_temperature(self, value: int) -> int:
        """Sets target temperate to desired value using Econet API."""
        resp = await self._target_temp.set_value(value)
        return resp

    @property
    def target_temperature_min(self) -> int:
        """Minimum value when setting target temperature."""
        return self._target_temp.minv

    @property
    def target_temperature_max(self) -> int:
        """Maximum value when setting target temperature."""
        return self._target_temp.maxv


class Mixer(TempController):
    def __init__(
        self,
        econet: Econet,
        current_temp: Params,
        target_temp: Params,
        valve: Params,
        pump: Params,
    ):
        super().__init__(econet, current_temp, target_temp)
        self._valve = Sensor(econet, valve)
        self._pump = Sensor(econet, valve)

    @property
    def valve(self) -> int:
        """Open percentage of the mixer valve"""
        return self._valve.value

    @property
    def pump(self) -> str:
        """Wheater pump is working"""
        return self._pump.value


class Smartfire(object):
    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username
        self.password = password
        self.sensors = dict()

    @property
    def econet(self) -> Econet:
        if hasattr(self, "_econet") is False:
            raise EconetUninitilized
        return self._econet

    @property
    def boiler(self) -> TempController:
        if (sensor := self.sensors.get("boiler")) is None:
            raise EconetUninitilized
        return sensor

    @property
    def huw(self) -> TempController:
        if (sensor := self.sensors.get("huw")) is None:
            raise EconetUninitilized
        return sensor

    @property
    def mixers(self) -> tuple:
        if not hasattr(self, "_mixers"):
            raise EconetUninitilized
        return self._mixers

    @property
    def operation_mode(self) -> str:
        if (sensor := self.sensors.get("operation_mode")) is None:
            raise EconetUninitilized
        return sensor

    @property
    def fuel_level(self) -> str:
        if (sensor := self.sensors.get("fuel_level")) is None:
            raise EconetUninitilized
        return sensor

    @property
    def fan(self) -> str:
        if (sensor := self.sensors.get("fan")) is None:
            raise EconetUninitilized
        return sensor

    @property
    def fan_speed(self) -> str:
        if (sensor := self.sensors.get("fan_speed")) is None:
            raise EconetUninitilized
        return sensor

    @property
    def feeder_temperature(self) -> str:
        if (sensor := self.sensors.get("feeder_temperature")) is None:
            raise EconetUninitilized
        return sensor

    @property
    def oxygen(self) -> str:
        if (sensor := self.sensors.get("oxygen")) is None:
            raise EconetUninitilized
        return sensor

    @property
    def huw_pump(self) -> str:
        if (sensor := self.sensors.get("huw_pump")) is None:
            raise EconetUninitilized
        return sensor

    @property
    def circulating_pump(self) -> str:
        if (sensor := self.sensors.get("circulating_pump")) is None:
            raise EconetUninitilized
        return sensor

    @property
    def boiler_pump(self) -> str:
        if (sensor := self.sensors.get("boiler_pump")) is None:
            raise EconetUninitilized
        return sensor

    @property
    def attributes(self) -> dict:
        return self._attrs

    async def update(self) -> None:
        if hasattr(self, "_econet") is False:
            self._econet = Econet(self.host, self.username, self.password)
            await self._econet.setup()
            self.sensors["boiler"] = TempController(
                self._econet,
                Params.BOILER_TEMPERATURE,
                Params.EDIT_PRESET_BOILER_TEMPERATURE,
            )
            self.sensors["huw"] = TempController(
                self._econet, Params.HUW_TEMPERATURE, Params.EDIT_HUW_PRESET_TEMPERATURE
            )
            mixers = list()
            mixers_params = [
                (
                    1,
                    Params.TEMP_MIXER_1,
                    Params.PRESET_MIXER_1,
                    Params.VALVE_MIXER_1,
                    Params.PUMP_MIXER_1,
                    Params.MIXER_1_SUPPORT,
                ),
                (
                    2,
                    Params.TEMP_MIXER_2,
                    Params.PRESET_MIXER_2,
                    Params.VALVE_MIXER_2,
                    Params.PUMP_MIXER_2,
                    Params.MIXER_2_SUPPORT,
                ),
                (
                    3,
                    Params.TEMP_MIXER_3,
                    Params.PRESET_MIXER_3,
                    Params.VALVE_MIXER_3,
                    Params.PUMP_MIXER_3,
                    Params.MIXER_3_SUPPORT,
                ),
                (
                    4,
                    Params.TEMP_MIXER_4,
                    Params.PRESET_MIXER_4,
                    Params.VALVE_MIXER_4,
                    Params.PUMP_MIXER_4,
                    Params.MIXER_4_SUPPORT,
                ),
            ]
            for mid, param, preset, valve, pump, supported in mixers_params:
                mixer = Mixer(self._econet, param, preset, valve, pump)
                if mixer.temperature is not None:
                    mixers.append(mixer)
            self._mixers = tuple(mixers)
            self.sensors["operation_mode"] = Sensor(self._econet, Params.OPERATION_MODE)
            self.sensors["summer_mode"] = Setting(self._econet, Params.SUMMER_MODE)
            self.sensors["alarm_level"] = Setting(self._econet, Params.ALARM_LEVEL)
            self.sensors["alarms"] = Sensor(self._econet, Params.ALARMS)
            self.sensors["fuel_level"] = Sensor(self._econet, Params.FUEL_LEVEL)
            self.sensors["fan"] = Sensor(self._econet, Params.FAN)
            self.sensors["fan_speed"] = Sensor(
                self._econet, Params.MINIMUM_AIRFLOW_OUTPUT
            )
            self.sensors["oxygen"] = Sensor(self._econet, Params.OXYGEN_2)
            self.sensors["feeder_temperature"] = Sensor(
                self._econet, Params.FEEDER_TEMPERATURE
            )
            self.sensors["huw_pump"] = Sensor(self._econet, Params.HUW_PUMP)
            self.sensors["circulating_pump"] = Sensor(
                self._econet, Params.CIRCULATING_PUMP
            )
            self.sensors["boiler_pump"] = Sensor(self._econet, Params.BOILER_PUMP)
            self.sensors["active_alarms"] = Sensor(self._econet, Params.ALARMS)
            self.sensors["emission_temperature"] = Sensor(
                self._econet, Params.EMISSION_TEMPERATURE
            )
            sys = await self._econet.fetch_sys_params()
            self._attrs = {
                "uid": sys["uid"],
                "ecosrvSoftVer": sys["ecosrvSoftVer"],
                "modulePanelSoftVer": sys["modulePanelSoftVer"],
                "moduleASoftVer": sys["moduleASoftVer"],
                "controllerID": sys["controllerID"],
                "settingsVer": sys["settingsVer"],
            }
        await self._econet.update()
