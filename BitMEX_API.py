import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


## Get all instruments OI



## Get just perp open interest

class BitMEXAPI(object):
    def __init__(self):
        self.url = 'https://www.bitmex.com/api/v1/'

    def request(self, action, params):
        # No API Key needed to access BFX Public API
        response = requests.get(self.url + action, params=params)
        # Catching errors
        if response.status_code != 200:
            raise Exception("Error: " + str(response.status_code) + "\n" + response.text + "\nRequest: " + response.url)

        json = response.json()
        return json

    def get_instrument_data(self, instrument):
        action = 'instrument'
        params = {"symbol": instrument}
        response = self.request(action, params)
        return response[0]

    def get_exchange_data_snapshot(self, currency=False):
        action = 'stats'
        params = ''
        response = self.request(action, params)
        if currency is not False:
            response = list(filter(lambda data: data['rootSymbol'] == currency, response))[0]
        return response





if __name__ == '__main__':
    btmx = BitMEXAPI()
    timestamp = datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%S')
    last_price = btmx.get_instrument_data('XBT')['lastPrice']
    open_interest_perp = btmx.get_instrument_data('XBT')['openInterest']
    open_interest_all = btmx.get_exchange_data_snapshot('XBT')['openInterest']
    perp_funding_rate = btmx.get_instrument_data('XBT')['fundingRate']



    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("BitMEX_Data").sheet1

    ## Update Sheet
    row_to_update = len(sheet.col_values(1))+1
    sheet.update_acell("A{}".format(row_to_update), timestamp)
    sheet.update_acell("B{}".format(row_to_update), last_price)
    sheet.update_acell("C{}".format(row_to_update), open_interest_perp)
    sheet.update_acell("D{}".format(row_to_update), open_interest_all)
    sheet.update_acell("E{}".format(row_to_update), perp_funding_rate)
    time.sleep(3600)
