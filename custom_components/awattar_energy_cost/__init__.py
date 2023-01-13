"""Component for EPEX Spot support."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_interval

from .const import (CONF_MARKET_AREA, CONF_TIMEZONE, CONF_VAT, CONF_ENERGYPLAN_ADDITION, DOMAIN)
from .Awattar_API import Awattar

_LOGGER = logging.getLogger(__name__)


PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up component from a config entry, config_entry contains data from config entry database."""
    # store shell object
    shell = hass.data.setdefault(DOMAIN, AwattarEnergyCost(hass))

    # add market area to shell
    shell.add_entry(entry)

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )
    if unload_ok:
        shell = hass.data[DOMAIN]
        shell.remove_entry(config_entry)
        if shell.is_idle():
            # also remove shell if not used by any entry any more
            del hass.data[DOMAIN]

    return unload_ok


class AwattarEnergyCost:
    """Shell object for Awattar Energy Cost. Stored in hass.data."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the instance."""
        self._hass = hass
        self._sources = {}

    def get_source(self, unique_id):
        return self._sources[unique_id]

    def add_entry(self, config_entry: ConfigEntry):
        """Add entry."""
        if self.is_idle():
            # This is the first entry, therefore start the timer
            self._fetch_callback_listener = async_track_time_interval(
                self._hass, self._fetch_callback, timedelta(hours=1)
            )

            # async_track_time_change(hass, action, hour=None, minute=None, second=None):

            source = Awattar(market_area=config_entry.data[CONF_MARKET_AREA],time_zone=config_entry.data[CONF_TIMEZONE],vat=config_entry.data[CONF_VAT], energyplan_addition=config_entry.data[CONF_ENERGYPLAN_ADDITION])
        
        self._hass.add_job(source.fetch)

        self._sources[config_entry.unique_id] = source

    def remove_entry(self, config_entry: ConfigEntry):
        """Remove entry."""
        self._sources.pop(config_entry.unique_id)

        if self.is_idle():
            # This was the last source, therefore stop the timer
            remove_listener = self._fetch_callback_listener
            if remove_listener is not None:
                remove_listener()

    def is_idle(self) -> bool:
        return not bool(self._sources)

    @callback
    def _fetch_callback(self, *_):
        self._hass.add_job(self._fetch)

    def _fetch(self, *_):
        for source in self._sources:
            try:
                self.get_source(source).fetch()
            except Exception as error:
                _LOGGER.error(f"fetch failed : {error}")
