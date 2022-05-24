from binance.client import Client
from binance_keys import api_key, secret_key   ## this is your own key saved in a seperate python filesimport time
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd


client = Client(api_key, secret_key)

coin = "BTC"

start_str = "Jan 31, 2021"
end_str = "Jul 21, 2022"

klines = client.get_historical_klines(symbol=f'{coin}USDT', 
                                          interval=client.KLINE_INTERVAL_1DAY, 
                                          start_str=start_str,
                                          end_str=end_str)

cols = ['DateTime',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'CloseTime',
            f'{coin}-QuoteAssetVolume',
            f'{coin}-NumberOfTrades', 
            f'{coin}-TBBAV',
            f'{coin}-TBQAV',
            f'{coin}-ignore']

coin_df  = pd.DataFrame(klines, columns=cols)
coin_df["DateTime"] = pd.to_datetime(coin_df["DateTime"], unit="ms") # Binance default to ms

coin_df.drop(['CloseTime', 'BTC-QuoteAssetVolume',
       'BTC-NumberOfTrades', 'BTC-TBBAV', 'BTC-TBQAV', 'BTC-ignore'], axis=1, inplace=True)

coin_df = coin_df.astype({
    "Open": float,
    "High": float,
    "Low": float,
    "Close": float,
    "Volume": float
})

coin_df.to_csv('BTC_Jan3121_Jul2121_1D.csv',index=False)

if __name__ == "__main__" :
    fig = go.Figure(data=[go.Candlestick(x=coin_df['DateTime'],
                open=coin_df['Open'],
                high=coin_df['High'],
                low=coin_df['Low'],
                close=coin_df['Close'])])

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()

