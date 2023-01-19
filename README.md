# Awattar Energy Cost

This project is widley based on and inspired by the work of Steffen Zimmermann: 
HA EPEX Spot - https://github.com/mampfes/ha_epex_spot - thx for this great custom component / base for my adaptions.


This component adds electricity prices for plans of Awattar (an German / Austrian energy provider)  to Home Assistant.

Therfore an api is provided from [Awattar](https://www.awattar.de/services/api) free of charge service for their customers. Market price data is available for Germany and Austria. So far no user identifiation is required.

## Installation

Note: this repo needs to be added to HACS store - until this is done, you can still install it using HACS by adding this repo as a "user defined" repository

1. Ensure that [HACS](https://hacs.xyz) is installed.
2. Install **Awattar Energy Cost** integration via HACS.
3. Add **Awattar Energy Cost** integration to Home Assistant:

   [![badge](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=awattar_energy_cost)

In case you would like to install manually:

1. Copy the folder `custom_components/awattar_energy_cost` to `custom_components` in your Home Assistant `config` folder.
2. Add **Awattar Energy Cost** integration to Home Assistant:

    [![badge](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=awattar_energy_cost)

## Sensors

This component provides one sensor for market prices. The sensor state is the current price in EUR-ct/kWh.

The sensor also allows to configure VAT and energy plan surcharge (charged by Awattar) to finally show the total price per kWh.

Also since the API of Awattar provides all timestamps based on UTC - therefore to correctly display the right price at a dedicated time, the timezone is required.

### Sensor Attributes

In addition to the current market price, the price sensor also provides a list of upcoming prices per hour:

```yaml
unit_of_measurement: ct/kWh
icon: mdi:currency-eur
friendly_name: Awattar at Price
data:
  - start_time: '2023-01-17T00:00:00+01:00'
    end_time: '2023-01-17T01:00:00+01:00'
    price_ct_per_kwh: 13.1
  - start_time: '2023-01-17T01:00:00+01:00'
    end_time: '2023-01-17T02:00:00+01:00'
    price_ct_per_kwh: 12.956
  - start_time: '2023-01-17T02:00:00+01:00'
    end_time: '2023-01-17T03:00:00+01:00'
    price_ct_per_kwh: 12.84
```