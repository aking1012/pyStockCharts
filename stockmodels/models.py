from django.db import models

'''
As there are more oscillators and overlays,
most will have pre-compute models and long running tasks to populate them.

The same is true of candlestick patterns.  As the finders are created, a
comprehensive historical index of found will become a database as well.
'''

class Exchanges(models.Model):
    exchange_name = models.CharField(max_length=30)
    exchange_data_url = models.CharField(max_length=255)

class Stock(models.Model):
    symbol = models.CharField(max_length=6)
    exchange = models.CharField(max_length=30)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=999, decimal_places=2)
    close_price = models.DecimalField(max_digits=999, decimal_places=2)
    adj_close = models.DecimalField(max_digits=999, decimal_places=2)
    high = models.DecimalField(max_digits=999, decimal_places=2)
    low = models.DecimalField(max_digits=999, decimal_places=2)
    volume = models.IntegerField()

class BaseStockInfo(models.Model):
    symbol = models.CharField(max_length=6)
    name = models.CharField(max_length=127)
    lastSale = models.DecimalField(max_digits=999, decimal_places=2)
    marketCap = models.DecimalField(max_digits=999, decimal_places=2)
    adr_tso =  models.DecimalField(max_digits=999, decimal_places=2)
    ipo_year = models.IntegerField()
    sector = models.CharField(max_length=127)
    subsector = models.CharField(max_length=127)
    summary = models.CharField(max_length=255)
    exchange = models.CharField(max_length=30)
    is_bad = models.NullBooleanField()
