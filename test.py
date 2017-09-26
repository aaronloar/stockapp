
import calculations
import test_data

print(len(test_data.data.keys()))

print("SMA:", calculations.sma(data=test_data.data, period=20))

sorted_keys = sorted(test_data.data.keys())

sum_gain, sum_loss = 0.00000000001, 0.000000000001
# avg_gain, avg_loss = 0, 0

period = 3

for k in range(1, period + 1):
    close = float(test_data.data[sorted_keys[k]]["4. close"])
    yest_close = float(test_data.data[sorted_keys[k - 1]]["4. close"])

    if close > yest_close:
        sum_gain += close - yest_close
    else:
        sum_loss += yest_close - close

    print("K: {}  Yest: {} {:.4f}  Date: {} {:.4f}  Gains: {:.4f}  Losses: {:.4f}".
          format(k, sorted_keys[k-1], yest_close, sorted_keys[k], close, sum_gain, sum_loss))

avg_gain = sum_gain / period
avg_loss = sum_loss / period

print("Gains: {:.4f}   Gains / period: {:.4f}".format(sum_gain, avg_gain))
print("Losses: {:.4f}  Losses / period: {:.4f}".format(sum_loss, avg_loss))

print(len(sorted_keys) - period)

rsi = 0

for i in range(period + 1, len(sorted_keys)):
    close = float(test_data.data[sorted_keys[i]]["4. close"])
    yest_close = float(test_data.data[sorted_keys[i - 1]]["4. close"])

    cur_gain, cur_loss = 0, 0

    if close > yest_close:
        cur_gain = close - yest_close
    else:
        cur_loss = yest_close - close

    avg_gain = ((avg_gain * (period - 1)) + cur_gain) / period
    avg_loss = ((avg_loss * (period - 1)) + cur_loss) / period

    rs = avg_gain / avg_loss

    rsi = (100 - (100 / (1 + rs)))

    print("I: {}  Yest: {} {:.4f}  Date: {} {:.4f} Gains: {:.4f} Losses: {:.4f} "
          "AvgGain: {:.4f} AvgLoss: {:.4f} RSI: {:.4f}".
          format(i, sorted_keys[i - 1], yest_close, sorted_keys[i], close, cur_gain, cur_loss,
                 avg_gain, avg_loss, rsi))

print("RSI({}): {:.4f}".format(period, rsi))
