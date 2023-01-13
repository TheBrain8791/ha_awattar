import logging
from datetime import datetime, timedelta, timezone
import pytz
import requests

_LOGGER = logging.getLogger(__name__)

class UtilTimeZone:
    timezone_name = ""
    
    def __init__(self,timezone_name):
        self.timezone_name = timezone_name
        
    def Get_TzUtcOffset(self):
        return timezone(pytz.timezone(self.timezone_name).localize(datetime.now()).utcoffset())

class Marketprice:
    UOM_EUR_PER_MWh = "EUR/MWh"
    UOM_CT_PER_KWh = "ct/kWh"

    def __init__(self, data, time_zone, vat, energyplan_addition):
        assert data["unit"].lower() == self.UOM_EUR_PER_MWh.lower()
        self._start_time = datetime.fromtimestamp(
            data["start_timestamp"] / 1000, tz=time_zone.Get_TzUtcOffset()
        )
        self._end_time = datetime.fromtimestamp(
            data["end_timestamp"] / 1000, tz=time_zone.Get_TzUtcOffset()
        )
        self._price_eur_per_mwh = float(data["marketprice"])
        self._price_vat = float(vat)
        self._price_energyplan_add = float(energyplan_addition)

    def __repr__(self):
        return f"{self.__class__.__name__}(start: {self._start_time.isoformat()}, end: {self._end_time.isoformat()}, marketprice: {self._price_ct_per_kwh} {self.UOM_CT_PER_KWh})"

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def price_eur_per_mwh(self):
        return self._price_eur_per_mwh * self._price_energyplan_add * self._price_vat

    @property
    def price_ct_per_kwh(self):
        return round(self._price_eur_per_mwh * self._price_energyplan_add * self._price_vat / 10 ,3)


class Awattar:
    URL = "https://api.awattar.{market_area}/v1/marketdata"

    MARKET_AREAS = ("at", "de")

    def __init__(self, market_area, time_zone, vat, energyplan_addition):
        self._market_area = market_area
        self._time_zone = UtilTimeZone(time_zone)  
        self._vat = vat
        self._energyplan_addition = energyplan_addition      
        self._url = self.URL.format(market_area=market_area)
        self._marketprices = []

    @property
    def name(self):
        return "Awattar API V1"

    @property
    def market_area(self):
        return self._market_area

    @property
    def marketprices(self):
        return self._marketprices

    def fetch(self):
        data = self._fetch_data(self._url)
        self._marketprices = self._extract_marketprices(data["data"])

    def _fetch_data(self, url):         
        start = datetime.now(tz=self._time_zone.Get_TzUtcOffset()).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end = start + timedelta(days=2)
        r = requests.get(url, params={"start": start, "end": end})
        r.raise_for_status()
        return r.json()

    def _extract_marketprices(self, data):
        entries = []
        for entry in data:
            entries.append(Marketprice(entry, self._time_zone, self._vat, self._energyplan_addition))
        return entries
