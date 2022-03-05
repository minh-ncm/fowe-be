import datetime
import time
from django.core.management.base import BaseCommand
import requests
import io
import pandas as pd
from cloudinary import uploader

from fowe.settings import ALPHA_VANTAGE_KEY
from ._utils import convert_datetime_timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        api_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED'
        symbols = pd.read_csv('stock/static/stock/us.csv', header=None).values.flatten()
        for symbol in symbols:
            symbol = symbol.upper()
            url = f'{api_url}&symbol={symbol}&interval=15min&slice=year1month1&apikey={ALPHA_VANTAGE_KEY}'
            time.sleep(12)
            response = requests.get(url)
            df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
            now = datetime.datetime.now()
            now = convert_datetime_timezone(now, 'UTC', 'Asia/Ho_Chi_Minh')
            now = now.strftime('%Y-%m-%d')
            path = f'temp/{symbol}#{now}.csv'
            df.to_csv(path, index=False, header=False)
            uploader.upload(path, folder='stock/us', resource_type='raw', use_filename=True, unique_filename=False)