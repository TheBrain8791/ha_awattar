#!/usr/bin/env python3

from Awattar_API import Awattar

service = Awattar(market_area="at",time_zone="Europe/Vienna", vat=20, energyplan_addition=3)
print(service.MARKET_AREAS)

service.fetch()
print(f"count = {len(service.marketprices)}")
for e in service.marketprices:
    print(f"{e.start_time}: {e.price_ct_per_kwh} {e.UOM_CT_PER_KWh}")
