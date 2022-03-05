from rest_framework.serializers import ModelSerializer

from stock.models import Stock


class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = ['code', 'time', 'open', 'high', 'low', 'close', 'volume']