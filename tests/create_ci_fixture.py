from pathlib import Path
import math
import pandas as pd

raw = Path('data/raw')
raw.mkdir(parents=True, exist_ok=True)

dates = pd.bdate_range('2025-01-02', periods=30)
tickers = ['AAPL','MSFT','JPM','XOM','JNJ','AMZN']
rows = []
for j,t in enumerate(tickers):
    base = 100 + 15*j
    for i,d in enumerate(dates):
        close = base * (1 + 0.002*i + 0.01*math.sin(i/4 + j))
        rows.append({'date':d.date(),'ticker':t,'open':close*0.995,'high':close*1.01,'low':close*0.99,'close':close,'adj_close':close,'volume':1_000_000 + i*1000 + j*10000})
pd.DataFrame(rows).to_csv(raw/'security_prices.csv', index=False)

bm=[]
for i,d in enumerate(dates):
    close=500*(1+0.0015*i+0.006*math.sin(i/5))
    bm.append({'date':d.date(),'ticker':'SPY','open':close*0.997,'high':close*1.008,'low':close*0.992,'close':close,'adj_close':close,'volume':50_000_000+i*5000})
pd.DataFrame(bm).to_csv(raw/'benchmark_prices.csv', index=False)
print('CI fixture created')
