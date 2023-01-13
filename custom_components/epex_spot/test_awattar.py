#!/usr/bin/env python3

from Awattar import Awattar_API

service = Awattar_API.Awattar(market_area="at")
print(service.MARKET_AREAS)

service.fetch()
print(f"count = {len(service.marketprices)}")
for e in service.marketprices:
    print(f"{e.start_time}: {e.price_ct_per_kwh} {e.UOM_CT_PER_KWh}")
