

def sma(data, period):
    """
    Calculate the Simple Moving Average of the last <span> days
    :param data: dictionary of data (format commented below)
    :param period: Number of days to calculate SMA
    :return: SMA, float value
    """

    d_sum = 0

    # Data Format (dictionary from JSON):
    # { '2000-07-28': { '1. open': '9.5000',
    #                   '2. high': '10.5000',
    #                   '3. low': '9.5000',
    #                   '4. close': '10.0600',
    #                   '5. volume': '1843300'},
    #   '2000-07-31': { '1. open': '10.0600',
    #                   '2. high': '10.8800',
    #                   '3. low': '10.0000',
    #                   '4. close': '10.2500',
    #                   '5. volume': '325800'},
    # ....

    for k in sorted(data.keys())[-period:]:  # Get last <span> days close value
        d_sum += float(data[k]['4. close'])

    return d_sum / period


def rsi(data, period):

    """
    Calculate the Relative Strength Index over the last <span> days
    :param data: dictionary of data
    :param period: number of days over which to calculate RSI
    :return: RSI, float value
    """

    sorted_keys = sorted(data.keys())

    sum_gain, sum_loss = 0.00000000001, 0.000000000001
    # avg_gain, avg_loss = 0, 0

    for k in range(1, period + 1):
        close = float(data[sorted_keys[k]]["4. close"])
        yest_close = float(data[sorted_keys[k - 1]]["4. close"])

        if close > yest_close:
            sum_gain += close - yest_close
        else:
            sum_loss += yest_close - close

        # print("K: {}  Yest: {} {:.4f}  Date: {} {:.4f}  Gains: {:.4f}  Losses: {:.4f}".
        #     format(k, sorted_keys[k - 1], yest_close, sorted_keys[k], close, sum_gain, sum_loss))

    avg_gain = sum_gain / period
    avg_loss = sum_loss / period

    print("Gains: {:.4f}   Gains / period: {:.4f}".format(sum_gain, avg_gain))
    print("Losses: {:.4f}  Losses / period: {:.4f}".format(sum_loss, avg_loss))

    print(len(sorted_keys) - period)
    _rsi = 0

    for i in range(period + 1, len(sorted_keys)):
        close = float(data[sorted_keys[i]]["4. close"])
        yest_close = float(data[sorted_keys[i - 1]]["4. close"])

        cur_gain, cur_loss = 0, 0

        if close > yest_close:
            cur_gain = close - yest_close
        else:
            cur_loss = yest_close - close

        avg_gain = ((avg_gain * (period - 1)) + cur_gain) / period
        avg_loss = ((avg_loss * (period - 1)) + cur_loss) / period

        rs = avg_gain / avg_loss

        _rsi = (100 - (100 / (1 + rs)))

        # print("I: {}  Yest: {} {:.4f}  Date: {} {:.4f} Gains: {:.4f} Losses: {:.4f} "
        #       "AvgGain: {:.4f} AvgLoss: {:.4f} RSI: {:.4f}".
        #       format(i, sorted_keys[i - 1], yest_close, sorted_keys[i], close, cur_gain, cur_loss,
        #              avg_gain, avg_loss, _rsi))

    print("RSI({}): {:.4f}".format(period, _rsi))
    return _rsi


