# Double_Bollinger_Band_with_Backtrader

This project is to demonstrate how to implement one kind of Technical Analysis "Double_Bollinger_Band" on CryptoCurrency . A trading strategy is built on the double bollinger band and it is backtested with the library `backtrader` and `QuantStats`. This projects is just to show the workflow but not advocate using it in real trading.  

## Pre-requisite
The python scripts are written for Python 3 only and specifically requires the two backtest modules <br>
1. backtrader
2. QuantStats

Install these 2 modules using `pip`
```
$ pip install backtrader
$ pip install quantstats --upgrade --no-cache-dir
```

## Understanding the scripts
1. `binance_keys.py`<br>
After opening an account in Binance, users need to input their own API keys here to gain access to the data through Binance API.

2. `gatherData.py` <br>
This script is to extract the daily data `interval=client.KLINE_INTERVAL_1DAY` of Bitcoin through Binance.To extract other intervals of trading data, users can choose the following Kline intervals
```
KLINE_INTERVAL_1MINUTE = '1m'
KLINE_INTERVAL_3MINUTE = '3m'
KLINE_INTERVAL_5MINUTE = '5m'
KLINE_INTERVAL_15MINUTE = '15m'
KLINE_INTERVAL_30MINUTE = '30m'
KLINE_INTERVAL_1HOUR = '1h'
KLINE_INTERVAL_2HOUR = '2h'
KLINE_INTERVAL_4HOUR = '4h'
KLINE_INTERVAL_6HOUR = '6h'
KLINE_INTERVAL_8HOUR = '8h'
KLINE_INTERVAL_12HOUR = '12h'
KLINE_INTERVAL_1DAY = '1d'
KLINE_INTERVAL_3DAY = '3d'
KLINE_INTERVAL_1WEEK = '1w'
KLINE_INTERVAL_1MONTH = '1M'
```
After running this script, the daily data of BTCUSD is plotted and a CSV file `BTC_Jan3121_Jul2121_1D.csv` is produced.

<img src="https://github.com/phynance/Double_Bollinger_Band_with_Backtest/blob/26b3451db567d883bfae2c3e7ee971bb86077d2c/BTC_Jan3121_Jul2121_1DPlot.png">


3. `main_double_bollinger.py` <br>
This main script creates a class `TestStrategy` inheriting from the BackTrader class `TestStrategy`, in which it can find the bollinger band automatically `self.bb = bt.indicators.BollingerBands()`.


The main idea of double bollinger band is similar to simply using bollinger band. It can be exemplified in the following block of code:

```
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
```

i. First of all, if the investor is not holding any asset, then the script will check if the lowest price of that day cross below the bottom of the bollinger band. If yes, the status `self.bottom` is set to `hit`. 
ii. After hitting the band's bottom, when the lowest price of any one following days bounce back above the bottom, the status is changed to `released`. 
iii. If the `released` status remains for 5 days, the status will be reset. However, if the lowest price of that day drops again below the band's bottom, a buy signal will be genereated.
iv. Similarly, the investor will sell out the asset when the highest price of any 2 trading days cross above the band's top. 

The exact logic can be exemplied in the following plot:

<img src="https://github.com/phynance/Double_Bollinger_Band_with_Backtest/blob/26b3451db567d883bfae2c3e7ee971bb86077d2c/DoubleBB_backtest1.png">


4. The idea is further backtested with Backtrader and the result is deeply analyzed by QuantStats `qs.reports.html(strat_return, output=True)`. A full report in HTML format is also generated. 
<img src="https://github.com/phynance/Double_Bollinger_Band_with_Backtest/blob/main/strategytearsheet.png">



## Follow-up:
In the study above, we can see that simply using double bollinger band will generate a quite unsatisfactory result. However, this whole projects builds up the skeleton for further ideas. 

1. For example, users may change the selling signal when crossing the middle of band instead of the top of the band. 
2. The valid period `self.buyreleasedDate+5` is set to 5 days in the example above. This may be trained further by Machine learning. 
3. This can be combineed with momemtum trading strategy or other indicators such as SMA, golden cross.
4. The script will be further extended to paper trading on Binance
