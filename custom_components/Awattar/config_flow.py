"""Config flow for EPEXSpot component.

Used by UI to setup integration.
"""
from typing import Optional
import voluptuous as vol
from homeassistant import config_entries

from .const import (CONF_ENERGYPLAN_ADDITION, CONF_MARKET_AREA, CONF_TIMEZONE, CONF_VAT,
                    DOMAIN)
from .Awattar_API import Awattar

CONF_DEFAULT_ENERGYPLAN_ADDITION = 3
CONF_DEFAULT_TIMEZONE = "Europe/Vienna"
CONF_DEFAULT_VAT = 20
class AwattarEnergyCostConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore
    """Component config flow."""

    VERSION = 1

    def __init__(self):
        self._source_name = None

    async def async_step_user(self, user_input=None):
        """Handle the start of the config flow.

        Called after integration has been selected in the 'add integration
        UI'. The user_input is set to None in this case. We will open a config
        flow form then.
        This function is also called if the form has been submitted. user_input
        contains a dict with the user entered values then.
        """
        
        areas = Awattar.MARKET_AREAS        

        data_schema = vol.Schema(
            {
                vol.Required(CONF_MARKET_AREA): vol.In(sorted(areas)),
                vol.Optional(CONF_TIMEZONE, default=CONF_DEFAULT_TIMEZONE): str,
                vol.Required(CONF_VAT, default=CONF_DEFAULT_VAT): vol.All(vol.Coerce(float), vol.Range(min=0,max=100)),
                vol.Required(CONF_ENERGYPLAN_ADDITION, default=CONF_DEFAULT_ENERGYPLAN_ADDITION): vol.All(vol.Coerce(float), vol.Range(min=0,max=100))
            }
        )

        return self.async_show_form(step_id="cfg_values", data_schema=data_schema)
                   

    async def async_step_cfg_values(self, user_input=None):
        if user_input is not None:
            # create an entry for this configuration
            market_area = user_input[CONF_MARKET_AREA]
            sel_timezone = user_input[CONF_TIMEZONE]
            apply_vat = user_input[CONF_VAT]
            apply_energyplan_add = user_input[CONF_ENERGYPLAN_ADDITION]
            title = f"Awattar ({market_area})"

            unique_id = f"{DOMAIN} Awattar {market_area}"
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=title,
                data={
                        CONF_MARKET_AREA: market_area, 
                        CONF_TIMEZONE: sel_timezone, 
                        CONF_VAT: apply_vat,
                        CONF_ENERGYPLAN_ADDITION: apply_energyplan_add
                    }
            )
