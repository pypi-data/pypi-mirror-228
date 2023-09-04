import pandas  as pd

def MACD(df, window_fast, window_slow, window_signal):
    macd = pd.DataFrame()
    macd['일자'] = df['일자']
    macd['ema_fast'] = df['종가'].ewm(span=window_fast).mean()
    macd['ema_slow'] = df['종가'].ewm(span=window_slow).mean()
    macd['macd'] = macd['ema_fast'] - macd['ema_slow']
    macd['signal'] = macd['macd'].ewm(span=window_signal).mean()
    macd['diff'] = macd['macd'] - macd['signal']
    macd['bar_positive'] = macd['diff'].map(lambda x: x if x > 0 else 0)
    macd['bar_negative'] = macd['diff'].map(lambda x: x if x < 0 else 0)
    
    return macd

def get_trade_signal(dfData):
    sig_list = []
    for idx, data in enumerate(dfData[['일자','diff']].values):
        if idx == 0:
            if data[1] > 0:
                sig_buy = 1

                sig_list.append([data[0], 'B'])
            else:
                sig_buy = -1            
        else:
            if data[1] * sig_buy < 0:
                if data[1] > 0:
                    sig_buy = 1
                    sig_list.append([data[0], 'B'])                
                else:
                    sig_buy = -1
                    sig_list.append([data[0], 'S'])       
    
#     for i in sig_list:
#         print(i)
    
    return pd.DataFrame(sig_list, columns=['일자','Signal'])


# def get_macd_trade_signal(macd):
#     sig_list = []
#     for idx, diff in enumerate(macd['diff']):
#         if idx == 0:
#             if diff > 0:
#                 sig_buy = 1
#             elif diff < 0:
#                 sig_buy = -1
#             else:
#                 sig_buy = -1

#             sig_list.append(' ')
#         else:
#             if diff * sig_buy < 0:
#                 if diff > 0:
#                     sig_buy = 1
#                     sig_list.append('B')                
#                 else:
#                     sig_buy = -1
#                     sig_list.append('S')                
#             else:
#                 sig_list.append(' ')       
    
# #     for i in sig_list:
# #         print(i)
    
#     return sig_list



def set_signal_for_backtest(dfTrade, dfSignal, pType = '종가', max_retention_days = 99999, multiRetentionInd = False):
    trade_idx = 0
    buy_idx = 0
    sell_idx = 0
    TRADE_CNT = len(dfTrade)
    last_sell_dt = '00000000'

    dfBacktestList = []
    dfBuyList  = dfSignal[dfSignal['Signal']=='B'][['일자','Signal']].sort_values('일자').values.tolist()
    dfSellList = dfSignal[dfSignal['Signal']=='S'][['일자','Signal']].sort_values('일자').values.tolist()

    
    while( buy_idx < len(dfBuyList) ):
        buy_dt = dfBuyList[buy_idx][0]
        buy_idx += 1
        
        # 주식 기보유 상태에서 재구매(multiRetentionInd==true) 여부 처리 로직 적용
        if (multiRetentionInd == False) and (buy_dt <= last_sell_dt):                 
            continue   

        while( (trade_idx < TRADE_CNT) and (dfTrade['일자'].iloc[trade_idx] < buy_dt) ):
            trade_idx += 1

        if trade_idx >= (TRADE_CNT - 1):  # 마지막 거래일에 B 시그널 버림
            break
        elif dfTrade['일자'].iloc[trade_idx] > buy_dt:
            print('(check!!) 일자 : ', dfTrade['일자'].iloc[trade_idx], ' vs 시그널적용일자 : ', buy_dt)
        else:
            buy_price = dfTrade[pType].iloc[trade_idx]
            trade_idx_buy = trade_idx
            sell_dt = None

            while( (sell_idx < len(dfSellList)) and sell_dt == None ):      
                if buy_dt < dfSellList[sell_idx][0]:
                    sell_dt = dfSellList[sell_idx][0]
                else:
                    sell_idx += 1

            if sell_dt == None:
                sell_dt = dfTrade['일자'].iloc[TRADE_CNT - 1]

            # 주식 최대 보유기간(max_retention_days) 로직 적용
            for i in range(trade_idx + 1, min(trade_idx + 1 + max_retention_days, TRADE_CNT)):
                if sell_dt == dfTrade['일자'].iloc[i]:
                    break
            
            sell_dt = dfTrade['일자'].iloc[i]
            sell_price = dfTrade[pType].iloc[i]
            trade_idx_sell = i

            dfBacktestList.append([trade_idx_buy, buy_dt, buy_price, trade_idx_sell, sell_dt, sell_price, sell_price/buy_price*100-100])
            last_sell_dt = sell_dt

    return pd.DataFrame(dfBacktestList, columns=['매수Idx','매수일자','매수가격','매도Idx','매도일자','매도가격','수익률(%)'])