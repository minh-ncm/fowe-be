from datetime import datetime
import uuid
import requests
import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand, CommandError

from stock.models import Stock
from ._utils import convert_datetime_timezone


class Command(BaseCommand):
    help = 'fetch stock price from vietnamese markets'

    def __get_symbols(self):
        df = pd.read_csv('stock/static/stock/vn.csv', header=None, keep_default_na=False)
        symbols = df.values.flatten()
        mask = np.where(symbols != '')
        return symbols[mask]

    def handle(self, *args, **options):
        time = datetime.now()
        time = convert_datetime_timezone(time, 'UTC', 'Asia/Ho_Chi_Minh')
        time = time.strftime('%Y/%m/%d %H:%M:00')
        url = 'https://bgapidatafeed.vps.com.vn/getliststockdata/'
        symbols = self.__get_symbols()
        response = requests.get(url+','.join(symbols))
        data = response.json()
        for value in data:        
            stock = Stock.objects.create(
                id= uuid.uuid1(),
                code = value.get('sym'),
                time = time,
                open = value.get('r'),
                high = value.get('highPrice'),
                low = value.get('lowPrice'),
                close = value.get('lastPrice'),
                volume = value.get('lot'),
                country= "VN",
            )
            stock.save()
