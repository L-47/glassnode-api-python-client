import json
import requests
import datetime
import iso8601
import pandas as pd
import os
#api calling options wip
api_items = [
{"assets": "https://api.glassnode.com/v2/metrics/endpoints"},
{"futures": ["https://api.glassnode.com/v1/metrics/derivatives/futures_volume_daily_latest",
"https://api.glassnode.com/v1/metrics/derivatives/futures_volume_daily_all_sum",
"https://api.glassnode.com/v1/metrics/derivatives/futures_open_interest_latest",
"https://api.glassnode.com/v1/metrics/derivatives/futures_open_interest_all_sum",
"https://api.glassnode.com/v1/metrics/derivatives/futures_open_interest_perpetual_sum",
"https://api.glassnode.com/v1/metrics/derivatives/futures_funding_rate_perpetual"
]}]
# use index of variables in get requests for ease of use
assets = api_items[0].values()
futures = api_items[1].values()
print(str(futures))

class GlassnodeClient:

    def __init__(self):
        self._api_key = os.environ.get("GLASSNODE_API_KEY")
        # check if api key is in env
        if self._api_key == None | self._api_key == "":
            os.environ["GLASSNODE_API_KEY"] = input(
                "api_key not found, please enter api_key: ")

    @property
    def api_key(self):
        return self._api_key

    def set_api_key(self, value):
        self._api_key = value

    def get(self, url, a='BTC', i='24h', c='native', s=None, u=None):
        p = dict()
        p['a'] = a
        p['i'] = i
        p['c'] = c

        if s is not None:
            try:
                p['s'] = iso8601.parse_date(s).strftime('%s')
            except ParseError:
                p['s'] = s

        if u is not None:
            try:
                p['u'] = iso8601.parse_date(u).strftime('%s')
            except ParseError:
                p['u'] = s

        p['api_key'] = self.api_key

        r = requests.get(url, params=p)

        try:
            r.raise_for_status()
        except Exception as e:
            print(e)
            print(r.text)

        try:
            df = pd.DataFrame(json.loads(r.text))
            df = df.set_index('t')
            df.index = pd.to_datetime(df.index, unit='s')
            df = df.sort_index()
            s = df.v
            s.name = '_'.join(url.split('/')[-2:])
            return s
        except Exception as e:
            print(e)
