from datetime import datetime
import aiohttp
from .params import Params
from .exceptions import EconetHTTPException, EconetUnauthorized, EconetUnknownId


class Param(object):
    def __init__(self, pid, data):
        self.desc = data.get("name", "")
        self.special = data.get("special", None)
        self.edit = data.get("edit", False)
        self.id = pid
        self.unit = data["unit"]
        self._value = data.get("value", None)
        self.minv = data.get("minv", None)
        self.maxv = data.get("maxv", None)
        self.offset = data.get("offset", None)
        self.mult = data.get("mult", None)
        self.enum = None

    @property
    def value(self):
        if self.enum is not None and self._value is not None:
            return self.enum[self._value]
        return self._value

    @value.setter
    def value(self, new):
        self._value = new

    def __str__(self):
        return f"{self.value}{self.unit if self.unit is not None else ''}"

    def __repr__(self):
        return f"{self.__class__.__name__}(pid={repr(self.id)})"


class Econet(object):
    def __init__(self, host, login, password):
        self.login = login
        self.password = password
        self.host = host
        self.params = dict()
        self.units = dict()
        self.enums = dict()

    def __repr__(self):
        return f"{self.__class__.__name__}(host={repr(self.host)}, login={repr(self.login)})"

    async def setup(self):
        self.units = await self.fetch_units()
        self.enums = await self.fetch_enums()
        self.alarms_names = await self.fetch_alarms_names()
        self.params = await self.fetch_current_data_params()
        self.params.update(await self.fetch_rm_params())
        await self.update()
        for param in self.params.values():
            if (
                param.special is not None
                and param.special != 0
                and param.value is not None
            ):
                if len(self.enums[param.special]["values"]) > param.value:
                    param.enum = self.enums[param.special]["values"]

    async def _call_api(self, cmd):
        async with aiohttp.ClientSession() as session:
            auth = aiohttp.BasicAuth(self.login, self.password)
            async with session.get(f"{self.host}/econet/{cmd}", auth=auth) as resp:
                if resp.status == 401:
                    raise EconetUnauthorized()
                if resp.status != 200:
                    raise EconetHTTPException(
                        f"Got {resp.status} {resp.reason} when calling "
                        f"{self.host}/econet/{cmd}"
                    )
                j = await resp.json()
                return j

    async def fetch_units(self):
        resp = await self._call_api("rmParamsUnitsNames")
        return resp["data"]

    async def fetch_enums(self):
        resp = await self._call_api("rmParamsEnums")
        return resp["data"]

    async def fetch_alarms_names(self):
        resp = await self._call_api("rmAlarmsNames")
        return resp["data"]

    async def fetch_current_data_params(self):
        resp = await self._call_api("rmCurrentDataParams")
        params = dict()
        for pid, data in resp["data"].items():
            data["unit"] = (
                self.units[int(data["unit"])]
                if int(data["unit"]) < len(self.units)
                else ""
            )
            if pid == "123":
                pid = "110"
            pid = Params.get_by_id(pid)
            params[pid] = Param(pid, data)
        return params

    async def fetch_rm_params(self):
        resp = await self._call_api("rmParamsData")
        params = dict()
        for pid, data in enumerate(resp["data"]):
            data["unit"] = (
                self.units[int(data["unit"])]
                if int(data["unit"]) < len(self.units)
                else ""
            )
            pid = Params.get_by_id(pid)
            params[pid] = Param(pid, data)
        return params

    async def fetch_sys_params(self):
        return await self._call_api("sysParams")

    async def fetch_reg_params_data(self):
        resp = await self._call_api("regParamsData")
        params_data = dict()
        for pid, data in resp["data"].items():
            PID = Params.get_by_id(pid)
            if PID is not None:
                params_data[PID] = data
        return params_data

    async def fetch_rm_params_data(self):
        resp = await self._call_api("rmParamsData")
        params_data = dict()
        for pid, data in enumerate(resp["data"]):
            PID = Params.get_by_id(pid)
            if PID is not None:
                params_data[PID] = data
        return params_data

    async def update(self):
        params_data = await self.fetch_reg_params_data()
        params_data.update(await self.fetch_rm_params_data())
        for pid, data in params_data.items():
            if pid not in self.params:
                continue
            if type(data) is dict:
                self.params[pid].special = data.get("special", None)
                self.params[pid].edit = data.get("edit", False)
                self.params[pid].value = data.get("value", None)
                self.params[pid].minv = data.get("minv", None)
                self.params[pid].maxv = data.get("maxv", None)
                self.params[pid].offset = data.get("offset", None)
                self.params[pid].mult = data.get("mult", None)
            else:
                self.params[pid].value = data

    async def get_active_alarms(self):
        sys_params = await self.fetch_sys_params()
        alarms = list()
        for alarm in sys_params["alarms"]:
            toDate = datetime.strptime(alarm["toDate"], "%Y-%m-%d %H:%M:%S")
            fromDate = datetime.strptime(alarm["fromDate"], "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            if toDate > now and now > fromDate:
                alarms.append(self.alarms_names["code"])
        return alarms

    def get_param(self, param):
        if (p := self.params.get(param)) is None:
            if type(param) != Params and Params.get_by_id(param) is None:
                raise EconetUnknownId(f"Unknow Parameter ID {param}.")
            undefined_data = dict(name=f"Undefined_{param}", unit="", value="Undefined")
            p = Param(param, undefined_data)
        return p

    async def set_param(self, param_id, value):
        if type(param_id) == int:
            endpoint = f"rmNewParam?newParamIndex={param_id}&newParamValue={value}"
        else:
            endpoint = f"rmCurrNewParam?newParamKey={param_id}&newParamValue={value}"
        resp = await self._call_api(endpoint)
        if resp["result"] != "OK":
            raise Exception(f"Something went wrong: {resp}")
