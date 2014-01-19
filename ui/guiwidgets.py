#!/usr/bin/env python
 
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

class stockDataWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

    def signals(self):
        pass
    def widgets(self):
        pass

'''
This should be called menuItems or something, not indicatorWidget...
but since a true indicatorwidget sub-classable isn't exposed, this is
the ugly we get.
'''

class indicatorWidget(Gtk.Menu):

    def menuitem_response(self, w, buf):
        print buf

    def __init__(self):
      Gtk.Menu.__init__(self)
          for i in range(3):
              buf = "Test-undermenu - %d" % i
           
              menu_item = Gtk.MenuItem(buf)
           
              self.append(menu_item)
          # this is where you would connect your menu item up with a function:
          # menu_items.connect("activate", menuitem_response, buf)
          # show the items
          self.show_all()

class allStockChartsWidgets:
    def __init__(self):
        self.indicator = AppIndicator.Indicator.new(
                        "example-simple-client",
                        "indicator-messages",
                        appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_attention_icon("indicator-messages-new")
        menu = indicatorWidget()
       
        self.indicator.set_menu(menu)


 
if __name__ == "__main__":
    my_widgets = allStockChartsWidgets()
    Gtk.main()