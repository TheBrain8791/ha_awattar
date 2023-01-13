# Awattar Energy Cost

This project is widley based on and inspired by the work of Steffen Zimmermann: 
HA EPEX Spot - https://github.com/mampfes/ha_epex_spot


This component adds electricity prices for plans of Awattar (an German / Austrian energy provider)  to Home Assistant.

Therfore an api is provided [Awattar](https://www.awattar.de/services/api) free of charge service for their customers. Market price data is available for Germany and Austria. So far no user identifiation is required.

## Installation

1. Ensure that [HACS](https://hacs.xyz) is installed.
2. Install **Awattar Energy Cost** integration via HACS.
3. Add **Awattar Energy Cost** integration to Home Assistant:

   [![badge](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=awattar_energy_cost)

In case you would like to install manually:

1. Copy the folder `custom_components/awattar_energy_cost` to `custom_components` in your Home Assistant `config` folder.
2. Add **EPEX Spot** integration to Home Assistant:

    [![badge](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=awattar_energy_cost)

## Sensors

This component provides one sensor for market prices. The sensor state is the current price in EUR-ct/kWh.

### Sensor Attributes

In addition to the current market price, the price sensor also provides a list of upcoming prices per hour:

```yaml
unit_of_measurement: ct/kWh
icon: mdi:currency-eur
friendly_name: Awattar
data:
  - start_time: '2022-12-15T23:00:00+00:00'
    end_time: '2022-12-16T00:00:00+00:00'
    price_ct_per_kwh: 29.63
  - start_time: '2022-12-16T00:00:00+00:00'
    end_time: '2022-12-16T01:00:00+00:00'
    price_ct_per_kwh: 28.812
  - start_time: '2022-12-16T01:00:00+00:00'
    end_time: '2022-12-16T02:00:00+00:00'
    price_ct_per_kwh: 28.19
```