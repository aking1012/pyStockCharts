import os, urllib, datetime, csv, datetime
from types import ListType, StringType
from stockmodels.models import *

'''
TODO add threading and locking to fetch many at once, but only sync one batch at a time.
TODO add callbacks to a gui update scaffold function for a progressbar for each task queue.
TODO many other things...
'''

def log(something):
    '''
    args
    [callback_type, content]

    A logger function.

    I'll connect it to a Glib schedule status callback eventually
    after all the data bits work, and I get to UI.
    '''
    print something

class YahooCsvHistorical:
    '''
    Class for fetching and updating historical stock database records
    from Yahoo!.
    '''
    def __init__(self, base_settings, callback=log):
        '''
        base_settings is a class with a settings dict to hold configuration parameters
        '''
        self.base_settings = base_settings
        self.callback = callback

    def last_trading_day(self):
        '''
        roll-back date to last closed trading day for db-syncs
        '''
        today = datetime.datetime.today()
        '''
        #TODO
        if before five PM EST - 1 day
        if datetime.datetime.now()??:
            today = date.today()-timedelta(days=1)
        '''
        if today.weekday() > 4:
            today = today-timedelta(days=6 - today.weekday())
        return today

    def fetch_symbol_historical(self, symbol, date_component):
        '''
        Symbol is the ticker symbol
        Date component is the bit at the end of the url, not date tuples
        '''
        print "Trying historical csv for: " + symbol
        base_url_historical = ''+\
            'http://ichart.finance.yahoo.com/table.csv?s='
        url = base_url_historical + symbol + date_component
        urllib.urlretrieve(url,
          os.path.join(self.base_settings.settings['folder'],
          'csvcache',
          symbol + ".csv"))

    def import_symbol_historical(self, symbol):
        '''
        This will be merged in to fetch once it is working...

        Read the csv
        Check if bad symbol
        Update is_bad
        Check for last date
        Import each row
        Delete csv from cache
        '''
        csvfile = os.path.join(self.base_settings.settings['folder'], 'csvcache', symbol + ".csv")
        try:
          with open(csvfile, 'r') as reader:
              record = BaseStockInfo.objects.get(symbol=symbol)
              if '<!doctype html' in reader.read():
                  print('bad')
                  record.is_bad = True
                  record.save()
              else:
                  try:
                      record.is_bad = False
                      record.save()
                  except:
                      print('Record could not save')
        except:
              record = BaseStockInfo.objects.get(symbol=symbol)
              record.is_bad = True
        if not record.is_bad:
            reader = csv.reader(open(csvfile, 'r').readlines())
            data = []
            for item in reader:
                data.append(list(item))
            first_row = data.pop(0)
            try:
                assert(first_row == ['Date',
                                    'Open',
                                    'High',
                                    'Low',
                                    'Close',
                                    'Volume',
                                    'Adj Close'])
                data.reverse()
                try:
                    last = Stock.objects.filter(symbol=symbol).order_by('date').last()
                    print("Found old data")
                    print("Integrating new data for symbol: " + symbol)

                except:
                    '''
                    You get here when there is no record for that symbol.
                    '''
                    print("Integrating new data for symbol: " + symbol)
                    exchange = BaseStockInfo.objects.get(symbol=symbol).exchange
                    #TODO insert get last pk in db and add to stock declaration
                    #Maybe - it should be an autofield the DB can generate for us...
                    commit = []
                    for item in data:
                        commit.append(Stock(symbol = symbol,
                                      exchange = exchange,
                                      date = item[0],
                                      open_price = item[1],
                                      high = item[2],
                                      low = item[3],
                                      close_price = item[4],
                                      volume = item[5],
                                      adj_close = item[6]))
                    Stock.objects.bulk_create(commit)
            except:
                return False
        return True

    def sync_symbols_historical(self):
        '''
        Sync data for all symbols in BaseStockInfo
        '''
        for symbol in BaseStockInfo.objects.all():
            if not symbol.is_bad:
                #set up dates
                #February 4, 1971 start date(first day NASDAQ market operated)
                start_date = (1971, 2, 4)
                today = datetime.date.today()
                end_date = (today.year, today.month, today.day)
                try:
                    o = Stock.objects.filter(symbol=symbol.symbol).order_by('date').last()
                    start_date = (o.date.year, o.date.month, o.date.day)
                except:
                    pass
                date_component = '&a='+str(start_date[1]-1)+\
                                 '&b='+str(start_date[2])+\
                                 '&c='+str(start_date[0])+\
                                 '&d='+str(end_date[1]-1)+\
                                 '&e='+str(end_date[2])+\
                                 '&f='+str(end_date[0])+\
                                 '&g=d'
                '''
                self.fetch_symbol_historical(symbol.symbol, date_component)
                '''
                self.import_symbol_historical(symbol.symbol)

    def fetch_symbol_list(self, exchange):
        '''
        Grab the symbol lists from the urls in the Exchanges record
        Populate the BaseStockInfo table
        '''
        print('Trying exchange: ' + exchange.exchange_name)
        if exchange.exchange_name in ['NASDAQ']:
            csvfile = urllib.urlopen(exchange.exchange_data_url)
            reader = csv.reader(csvfile, quotechar='"')
            first_row = reader.next()
            try:
                assert(first_row == ['Symbol',
                                    'Name',
                                    'LastSale',
                                    'MarketCap',
                                    'ADR TSO',
                                    'IPOyear',
                                    'Sector',
                                    'industry',
                                    'Summary Quote',
                                    ''])
            except:
                return False
            for row in reader:
                symbol = row[0]
                print("Trying symbol: " + symbol)
                if not BaseStockInfo.objects.filter(symbol=symbol).exists():
                    j=0
                    for item in row:
                      if item == 'n/a' and j in [2,3,4,5]:
                          row[j]=0
                      j+=1
                    BaseStockInfo(symbol=symbol,
                                  name=row[1],
                                  lastSale=float(row[2]),
                                  marketCap=float(row[3]),
                                  adr_tso=float(row[4]),
                                  ipo_year=int(row[5]),
                                  sector=row[6],
                                  subsector=row[7],
                                  summary=row[8],
                                  exchange=exchange.exchange_name,
                                  ).save()
        return True

    def fetch_all(self):
        '''
        Fetch the base market ticker lists
        Fetch the historical CSVs
        Merge them in to the database
        '''
        for exchange in Exchanges.objects.all():
            if not self.fetch_symbol_list(exchange):
                print('CSV format changed... bailed out.')
        self.sync_symbols_historical()

    def find_splits(self, symbol, start_date, end_date):
        '''
        example url:
        http://ichart.finance.yahoo.com/x?s=IBM&a=00&b=2&c=1962&d=04&e=25&f=2011&g=v&y=0&z=30000
        '''
        base_url = 'http://ichart.finance.yahoo.com/x?'
        s=smybol
        if not start_date:
              #February 4, 1971 start date(first day NASDAQ market operated)
              #I only care about NASDAQ stocks for my own reasons...
              start_date = datetime.date(1971, 4, 1).timetuple()
        if not end_date:
              #today
              end_date = datetime.datetime.today().timetuple()

              date_component = '&a='+str(start_date[1]-1)+\
                              '&b='+str(start_date[2]-1)+\
                              '&c='+str(start_date[0])+\
                              '&d='+str(end_date[1]-1)+\
                              '&e='+str(end_date[2]-1)+\
                              '&f='+str(end_date[0])+\
                              '&g=v&y=0&z=30000'
        return False