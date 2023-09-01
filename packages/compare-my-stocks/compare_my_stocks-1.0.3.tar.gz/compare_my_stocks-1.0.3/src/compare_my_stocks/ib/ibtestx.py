import logging
import logging
import math
import time
import datetime
from collections import defaultdict
from requests import HTTPError

import flask
import numpy
from flask import request
from flask import Flask

from config import config
from input.ibsource import IBSource
#from config import config


flaskapp = Flask('ibtest')

# Create a new session of the IB Web API.

GLOB_DIC=defaultdict( dict)
HIST_PERIOD='1m'
MAX_DIFF=60 #seconds
PORT=8080
# grab the account data.

class IBMediator():
    def __init__(self):
        self._ibsource : IBSource=IBSource()

    def grep_positions_value(self,added_qty=0,buy_price=0,override=0):
        positions= self._ibsource.get_positions()
        for w in positions:
            yield self.get_updated_dict(w)
        # k = 0
        # cont = True
        # while (cont):
        #
        #
        #
        #     cont = (len(positions) == 30)  # max in page


    def get_updated_dict(self,w):
        stat=''
        tim = datetime.datetime.now()


        tick=self._ibsource.get_realtime_contract(w['contract'])
        last= tick.last
        open= tick.open

        mktval=last* w['position']


        v = {"Sym":w['contractDesc'], "Qty": w["position"], "Last": last , "RelProfit": 0, "Value": mktval,
             'Currency': w['currency'], 'Crypto': 0, 'Open': open, 'Source': 'IB', 'AvgConst': w['avgCost'],
             }

        return v


@flaskapp.route("/get_account_data")
def get_account_data():
    return {'data': list(mediator.grep_positions_value(config.REGULAR_ACCOUNT))}

mediator=None 
def main(runFalsk=True):
    global mediator
    mediator=IBMediator()
    # create a new session.
    #acc = ib_client.portfolio_accounts()
    #acc2 = ib_client.server_accounts()
    if not runFalsk:
        return
    if 1:
        logging.debug((get_account_data()))
    else:
        flaskapp.run(debug=True, port=PORT)


# @flaskapp.route("/get_symbol_history")
# def get_symbol_history(name,period,interval):
    # condid=lookup_symbol(name)
    # if not condid:
        # return  None
    # try:

        # hist = ib_client.market_data_history(condid,period, interval)['data']
    # except:
        # logging.debug(('failed getting data %s' % name ))
        # return None
    # return hist


if __name__ == '__main__':
    main()
