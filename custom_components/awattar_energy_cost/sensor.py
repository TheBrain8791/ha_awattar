import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (ATTR_IDENTIFIERS, ATTR_MANUFACTURER,
                                 ATTR_MODEL, ATTR_NAME)
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.util.dt import utcnow

from .const import DOMAIN

ATTR_DATA = "data"

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up platform for a new integration.

    Called by the HA framework after async_setup_platforms has been called
    during initialization of a new integration.
    """
    shell = hass.data[DOMAIN]
    unique_id = config_entry.unique_id

    entities = []

    entities.append(
        AwattarEnergyPriceSensorEntity(hass, shell.get_source(unique_id), unique_id)
    )
    
    async_add_entities(entities)


class AwattarSpotSensorEntity(SensorEntity):
    """Home Assistant sensor containing all Awattar spot data."""

    def __init__(self, hass, source):
        self._source = source
        self._value = None

        self._attr_device_info = {
            ATTR_IDENTIFIERS: {(DOMAIN, f"{source.name} {source.market_area}")},
            ATTR_NAME: "Awattar Spot Data",
            ATTR_MANUFACTURER: source.name,
            ATTR_MODEL: source.market_area,
            "entry_type": DeviceEntryType.SERVICE,
        }

    @property
    def available(self):
        """Return true if value is valid."""
        return self._value is not None

    @property
    def native_value(self):
        """Return the value of the entity."""
        return self._value

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return "ct/kWh"


class AwattarEnergyPriceSensorEntity(AwattarSpotSensorEntity):
    """Home Assistant sensor containing all Awattar price """

    def __init__(self, hass, source, unique_id):
        AwattarSpotSensorEntity.__init__(self, hass, source)
        self._attr_unique_id = f"{unique_id} Price"
        self._attr_name = f"Awattar {source.market_area} Price"
        self._attr_icon = "mdi:currency-eur"

    async def async_update(self):
        """Update the value of the entity."""
        now = utcnow()

        self._value = None

        data = []

        for e in self._source.marketprices:
            # find current value
            if e.start_time <= now and e.end_time > now:
                self._value = e.price_ct_per_kwh

            info = {
                "start_time": e.start_time.isoformat(),
                "end_time": e.end_time.isoformat(),
                "price_ct_per_kwh": e.price_ct_per_kwh,
            }
            data.append(info)

        attributes = {
            ATTR_DATA: data,
        }
        self._attr_extra_state_attributes = attributes

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return "ct/kWh"

