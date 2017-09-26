
import calculations
import test_data

period = 14

print("SMA: ", calculations.sma(data=test_data.data, period=20))
print("RSI: ", calculations.rsi(data=test_data.data, period=3))

sorted_keys = sorted(test_data.data.keys())

t_hi = float(test_data.data[sorted_keys[-1]]['2. high'])
t_lo = float(test_data.data[sorted_keys[-1]]['3. low'])
y_c = float(test_data.data[sorted_keys[-2]]['4. close'])

tr1 = t_hi - t_lo  # Today's high - today's low
tr2 = abs(t_hi - y_c)   # Today's high - yesterday's close
tr3 = abs(y_c - t_lo)   # Yesterday's close - today's low

tr = max(tr1, tr2, tr3)  # The max of the three TRs

print("TR1: {:.4f}  TR2: {:.4f}  TR3: {:.4f}  TR: {:.4f}".format(tr1, tr2, tr3, tr))

atr = 0
# loop through sorted_keys, starting at second
# oldest entry (because we need yesterday's close)
for i in range(1, period + 1):
    t_hi = float(test_data.data[sorted_keys[i]]['2. high'])
    t_lo = float(test_data.data[sorted_keys[i]]['3. low'])
    y_c = float(test_data.data[sorted_keys[i - 1]]['4. close'])

    tr1 = t_hi - t_lo  # Today's high - today's low
    tr2 = abs(t_hi - y_c)  # Today's high - yesterday's close
    tr3 = abs(y_c - t_lo)  # Yesterday's close - today's low

    tr = max(tr1, tr2, tr3)  # The max of the three TRs

    atr += tr  # Sum tr's for the first period days

    print("i: {}  tr: {}  atr: {}".format(i, tr, atr))

atr /= period
print("ATR: {}  Period: {}".format(atr, period))

for i in range(period + 1, len(sorted_keys)):
    t_hi = float(test_data.data[sorted_keys[i]]['2. high'])
    t_lo = float(test_data.data[sorted_keys[i]]['3. low'])
    y_c = float(test_data.data[sorted_keys[i - 1]]['4. close'])

    tr1 = t_hi - t_lo  # Today's high - today's low
    tr2 = abs(t_hi - y_c)  # Today's high - yesterday's close
    tr3 = abs(y_c - t_lo)  # Yesterday's close - today's low

    tr = max(tr1, tr2, tr3)  # The max of the three TRs

    atr = ((atr * (period - 1)) + tr) / period

print("ATR: {}".format(atr))
