import backtrader as bt
import backtrader.feeds as btfeeds
# from click import style
import pandas as pd
import quantstats as qs

coin_df = pd.read_csv('BTC_Jan3121_Jul2121_1D.csv')

coin_df["DateTime"] = pd.to_datetime(coin_df["DateTime"], format="%Y/%m/%d") # Binance default to ms

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.bb = bt.indicators.BollingerBands()
        self.bottom = "none"
        self.top = "none"
        self.reset_bottom()
        self.reset_top()
        self.order = None

    def reset_bottom(self):
        self.bottom = "none"

    def reset_top(self):
        self.top = "none"
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None
    
    def next(self):
        if self.order:
            return
        # self.log('Low, %.2f' % self.data.lines.low[0])
        #print(len(self))
        #print(self.order)
        #print(self.position)

        if not self.position:    #check buy condition
            if self.bottom == "hit" and self.data.lines.low[0] > self.bb.lines.bot[0]:
                    self.bottom = "released"
                    self.buyreleasedDate = len(self)
                    print("released")
            if  self.bottom == "released" and len(self) > self.buyreleasedDate+5:  # the status "released" only remains valid within 5 days
                    self.reset_bottom()
                    print('Reset')
            if self.data.lines.low[0] < self.bb.lines.bot[0]: 
                if self.bottom == "released":
                    self.reset_bottom()
                    self.order = self.buy()
                    print('Reset')
                else:
                    self.bottom = "hit"
                    print('Bottom Hit')

        else: # if holding the asset already
             if self.top == "hit" and self.data.lines.high[0] < self.bb.lines.top[0]:
                     self.top = "released"
             if self.data.lines.high[0] > self.bb.lines.top[0]:
                 if self.top == "released":
                     self.reset_bottom()
                     self.order = self.sell()
                 else:
                     self.top = "hit"

cerebro = bt.Cerebro()
cerebro.addstrategy(TestStrategy)


class PandasData(bt.feeds.PandasData):
    params = (
        ("datetime", "DateTime"),
        ('open','Open'),
        ('high','High'),
        ('low','Low'),
        ('close','Close'),
        ('volume','Volume'),
        ('openinterest',None)
    )
bt_df = cerebro.adddata(PandasData(dataname=coin_df))
cerebro.broker.setcash(100000.0)

#use pyfolio for performance and risk analysis
# cerebro.addanalyzer(bt.analyzers.PyFolio, _name="pyfolio")
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name="return")

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
results = cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

strat = results[0]
strat_return = strat.analyzers.getbyname("return").get_analysis()
strat_return = list(strat_return.items())
idx, values = zip(*strat_return)
strat_return = pd.Series(values, idx)

qs.reports.html(strat_return, output=True)


# import pyfolio as pf
# pf.create_full_tear_sheet(
#     returns,
#     positions=positions,
#     transactions=transactions,
#     live_start_date="2021-02-05",
#     round_trips=True
# )

cerebro.plot(style = 'candlestick', barup = '#ff9896', bardown='#98df8a')



# cerebro = bt.Cerebro(stdstats=False)

# cerebro.addstrategy(bt.Strategy)




