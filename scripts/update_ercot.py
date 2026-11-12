from datetime import datetime, timedelta, timezone
from pathlib import Path
from gridstatusio import GridStatusClient

client = GridStatusClient()  # gets GRIDSTATUS_API_KEY from environment

# Retrieve the three previous complete UTC days.
end = datetime.now(timezone.utc).date()
start = end - timedelta(days=3)

prices = client.get_dataset(
    dataset="ercot_spp_real_time_15_min",
    start=str(start),
    end=str(end),
    filter_column="location",
    filter_value=[
        "LZ_HOUSTON", "LZ_NORTH", "LZ_SOUTH", "LZ_WEST"
    ],
    filter_operator="in",
    timezone="US/Central",
)

if prices.empty:
    raise RuntimeError("No data returned: check dates and API access")

out = Path("data/ercot_spp.csv")
out.parent.mkdir(parents=True, exist_ok=True)
prices.to_csv(out, index=False)
print(f"Saved {len(prices):,} rows to {out}")
