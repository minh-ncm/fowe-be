from django.db import models


class Stock(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    code = models.CharField(max_length=10)
    time = models.CharField(max_length=20)
    open = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    high = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    low = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    close = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    country = models.CharField(max_length=2)