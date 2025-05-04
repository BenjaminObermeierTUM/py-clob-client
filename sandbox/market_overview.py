import os
from py_clob_client.constants import POLYGON
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs
from py_clob_client.order_builder.constants import BUY

from py_clob_client.clob_types import ApiCreds, BalanceAllowanceParams, AssetType
from dotenv import load_dotenv
from py_clob_client.constants import AMOY
from datetime import datetime, timedelta, timezone

# Load environment variables from .env file
load_dotenv()

host = "https://clob.polymarket.com"
key = os.getenv("PK")
chain_id = POLYGON

# Create CLOB client and get/set API credentials
client = ClobClient(host, key=key, chain_id=chain_id)
client.set_api_creds(client.create_or_derive_api_creds())

print(client.get_ok())

'''
#get balance allowance
collateral = client.get_balance_allowance(
    params=BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
)
print(collateral)



# Fetch all markets
markets = client.get_markets()

# Get current UTC time
now = datetime.now(timezone.utc)
in_48h = now + timedelta(hours=48)

print(markets['data'][0:10])
print(markets['next_cursor'])
resp = client.get_markets(next_cursor = markets['next_cursor'])
print(resp['data'][0:10])
print(resp['next_cursor'])
print(resp['data'][0]['end_date_iso'])

'''

def get_markets_ending_in_next_5_days(client):
    """
    Returns a list of all markets ending in the next 5 days (UTC).
    Uses the count property to avoid unnecessary pagination.
    """
    from datetime import datetime, timedelta, timezone

    now = datetime.now(timezone.utc)
    in_5_days = now + timedelta(days=5)
    result = []
    next_cursor = None
    total_count = None
    seen = 0

    while True:
        # Fetch markets with or without next_cursor
        if next_cursor:
            markets_resp = client.get_markets(next_cursor=next_cursor)
        else:
            markets_resp = client.get_markets()
            first_count = markets_resp.get('count')  # Only set on first call

        markets = markets_resp.get('data', [])
        if not markets:
            break

        for market in markets:
            end_date_iso = market.get('end_date_iso')
            if end_date_iso:
                try:
                    end_dt = datetime.fromisoformat(end_date_iso.replace("Z", "+00:00"))
                    if now <= end_dt <= in_5_days:
                        result.append(market)
                except Exception as e:
                    print(f"Error parsing date for market {market.get('condition_id')}: {e}")

        seen += len(markets)
        next_cursor = markets_resp.get('next_cursor')
        count = markets_resp.get('count')
        print(next_cursor, count)

        if first_count > count:
            break
        # If we've seen all markets or next_cursor is missing, stop
        #if not next_cursor or (total_count is not None and seen >= total_count):
        #    break

    return result

# Usage example:
markets_ending_soon = get_markets_ending_in_next_5_days(client)

for market in markets_ending_soon:
    print(market)

print(f"Markets ending in the next 5 days: {len(markets_ending_soon)}")



