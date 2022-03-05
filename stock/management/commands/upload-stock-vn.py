import os
from datetime import datetime
from django.core.management.base import BaseCommand
from cloudinary import uploader
import pandas as pd

from stock.models import Stock
from stock.serializers import StockSerializer
from ._utils import convert_datetime_timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        date = datetime.now()
        date = convert_datetime_timezone(date, 'UTC', 'Asia/Ho_Chi_Minh')
        date = date.strftime("%Y-%m-%d")
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        data = [record.values() for record in serializer.data]
        df = pd.DataFrame(data)
        file = os.path.join('temp', f'{date}.csv')
        df.to_csv(file, header=False, index=False)
        try:
            response = uploader.upload(file, folder='stock/vn', resource_type='raw', use_filename=True, unique_filename=False)
        except Exception:
            pass
        else:
            stocks.delete()