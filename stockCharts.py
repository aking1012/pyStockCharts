'''
The beginnings of more work than any human would care to do...
'''
import os, argparse

'''
Trying to maintain Windows compatibility with minimal effort/divergence...

Hopefully I can get a VPS with enough space to just let some of these huge
tasks and huge databases just grind and pre-compute.
'''

#Base settings for the app itself
class BaseSettings:
    def __init__(self):
        '''
        If I didn't plan on moving to mongo, hadoop, or postgres - or keeping it in user,
        so it works on Windows, but poorly... I would put the files in /opt.
        '''
        self.settings = {}
        self.settings['home'] = os.path.expanduser('~')
        self.settings['folder'] = os.path.join(self.settings['home'], '.stockCharts')
        self.settings['db_file'] = os.path.join(self.settings['folder'], 'scdb.sqlite3')

base_settings = BaseSettings()

#Make sure crap exists...
def mkdirs(dirs):
    for a_dir in dirs:
        try:
            os.mkdir(a_dir)
        except:
            pass

mkdirs([base_settings.settings['folder'],
    os.path.join(base_settings.settings['folder'], 'csvcache'),
    ])

#Get the Django ORM set up
from django.conf import settings
from django.core.management import execute_from_command_line

#Django settings
settings.configure(DEBUG=False,
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': base_settings.settings['db_file'],
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    },
    INSTALLED_APPS = ('stockmodels',)
)

from dataacquisition import fetch
historical = fetch.YahooCsvHistorical(base_settings)

def purge():
    '''
    '''
    try:
        os.remove(base_settings.settings['db_file'])
    except:
        '''
        You can get here if the file doesn't exist...
        '''
        pass
def sync():
    '''
    '''
    crap = ['manage.py', 'syncdb']
    execute_from_command_line(crap)

def add_exchanges():
    '''
    '''
    from stockmodels.models import Exchanges
    Exchanges(exchange_name = 'NASDAQ',
              exchange_data_url =  'http://www.nasdaq.com/'+\
              'screening/companies-by-name.aspx?'+\
              'letter=0&exchange=nasdaq&render=download').save()

def initialize():
    '''
    '''
    purge()
    sync()
    add_exchanges()

def update():
    '''
    '''
    historical.fetch_all()

if __name__ == '__main__':
    '''
    When the GUI is complete, launching with no args will launch the GUI
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-h", "--help",
        help="print help",
        action="store_true")
    parser.add_argument("-p", "--purge",
        help="purge db",
        action="store_true")
    parser.add_argument("-s", "--sync",
        help="sync models",
        action="store_true")
    parser.add_argument("-a", "--add_exchanges",
        help="add exchanges",
        action="store_true")
    parser.add_argument("-i", "--initialize",
        help="purge everything and rebuild a clean database",
        action="store_true")
    parser.add_argument("-u", "--update",
        help="update the CSV cache",
        action="store_true")
    args = parser.parse_args()
    if args.update:
        print "Trying to update the cache"
        update()
    if args.purge:
        print "Trying to import the databse"
        purge()
    if args.sync:
        print "Trying to sync models"
        sync()
    if args.add_exchanges:
        print "Trying to add exchanges"
        add_exchanges()
    if args.initialize:
        print "Trying to add exchanges"
        initialize()
    if args.update:
        print "Trying to add exchanges"
        update()