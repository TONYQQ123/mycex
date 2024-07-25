from pybit.unified_trading import HTTP
import pybit
import json

class mybybit():
    # def __init__(self):
    #     with open('bybitConfi.json') as f:
    #         confi=json.load(f)

    #     apikey = confi['api_key']
    #     secretkey = confi['secretkey']
    #     flag=confi['flag']
    #     f=False
    #     if flag=='1':
    #         f=True
    #     self.session = HTTP(
    #         demo=f,
    #         api_key=apikey,
    #         api_secret=secretkey,
    #     )
    def __init__(self,api,secret,password,demo):
        flag=demo
        f=False
        if flag=='1':
            f=True
        self.session = HTTP(
            demo=f,
            api_key=api,
            api_secret=secret,
        )

    def balance(self,ccy):
        result=None
        if ccy!='':
            target=f"USDT,USDC,{ccy}"
        else:
            target=f"USDT,USDC"
        result = None

        try:
            result = self.session.get_wallet_balance(accountType="UNIFIED",coin=target)
        except pybit.exceptions.FailedRequestError as e:
            print(f"Failed to get wallet balance: {e}")
            
        res={
            'msg':result['retMsg'],
            'code':str(result['retCode'])
        }
        if result['retCode']!=0:
            return res

        result=result['result']['list'][0]
        total=result.get('totalAvailableBalance')
        detail=result.get('coin')
        USDT_ava='0'
        USDC_ava='0'
        #breakpoint()
        target='0'
        for data in detail:
            if data.get('coin')==ccy:
                target=data.get('walletBalance','0')
            if data.get('coin')=='USDT':
                USDT_ava=data.get('walletBalance','0')
            if data.get('coin')=='USDC':
                USDC_ava=data.get('walletBalance','0')
        res={
            'total':total,
            'USDT':USDT_ava,
            'USDC':USDC_ava,
            ccy:target
        }
        return res
    
    def position(self,symbol):
        result=None
        try:
            result=self.session.get_positions(
                category="linear",
                symbol=symbol,
            )
        except pybit.exceptions.FailedRequestError as e:
            print(f"Failed to get wallet balance: {e}")

        res={
            'msg':result['retMsg'],
            'code':str(result['retCode'])
        }
        if result['retCode']!='0':
            return res

        data=result['result']['list'][0]
        
        res['ccy'] = data.get('symbol')
        res['num'] = data.get('size')
        res['avgprice'] = data.get(' avgPrice')
        res['gain'] = data.get('unrealisedPnl')
        res['closed'] = data.get('liqPrice')  # 强平价
        res['margin'] = data.get('positionBalance')  # 保证金
        return res
    
    def setLever(self,instId,lever):
        result=None
        try:
            result = self.session.set_leverage(
            category="linear",
            symbol=instId,
            buyLeverage=lever,
            sellLeverage=lever,
        )
        except pybit.exceptions.FailedRequestError as e:
            print(f"Failed to get wallet balance: {e}")

        res={
            'msg':result['retMsg'],
            'code':str(result['retCode'])
        }
        return res
    

    def fundingRatio(self,instId):
        result=None
        try:
            result = HTTP(demo=True).get_tickers(
            category="inverse",
            symbol=instId,)
        except pybit.exceptions.FailedRequestError as e:
            print(f"Failed to get wallet balance: {e}")

        res={
            'msg':result['retMsg'],
            'code':str(result['retCode'])
        }
        if result['retCode']!=0:
            return res
        result=result['result']['list'][0]
        res['ratio']=result['fundingRate']
        res['nextTime']=result['nextFundingTime']  
        return res
    
    def price(self,instId):
        result=None
        try:
            result = HTTP(demo=True).get_tickers(
            category="inverse",
            symbol=instId,)
        except pybit.exceptions.FailedRequestError as e:
            print(f"Failed to get wallet balance: {e}")

        res={
            'msg':result['retMsg'],
            'code':str(result['retCode'])
        }
        if result['retCode']!=0:
            return res
        result=result['result']['list'][0]
        res['price']=result['lastPrice']
        return res
    
    def bybitTime(self):
        result=None
        try:
            result = HTTP(demo=True).get_server_time()
        except pybit.exceptions.FailedRequestError as e:
            print(f"Failed to get wallet balance: {e}")

        res={
            'msg':result['retMsg'],
            'code':str(result['retCode'])
        }
        if result['retCode']!=0:
            return res
        res['time']=result['time']
        return res


    '''
    timeInForce策略:
    GTC 一直有效至取消
    IOC 立即成交或取消
    FOK 完全成交或取消
    PostOnly: 被動委托類型，如果該訂單在提交時會被立即執行成交，它將被取消. 
    這樣做的目的是為了保護您的訂單在提交的過程中，如果因為場內的價格變化，
    而撮合系統無法委託該筆訂單到訂單簿，因此會被取消。針對 PostOnly 訂單類型，
    單筆訂單可提交的數量比其他類型的訂單更多，
    請參考該接口中的lotSizeFilter > postOnlyMaxOrderQty參數.


    marketUnit	false	string	統一帳戶現貨交易創建市價單時給入參qty指定的單位, 支持orderFilter=Order, tpslOrder 和 StopOrder
    baseCoin: 比如, 買BTCUSDT, 則"qty"的單位是BTC
    quoteCoin: 比如, 賣BTCUSDT, 則"qty"的單位是USDT
    '''
    def trade(self,instId,side,ordType,price,sz):
        result=None
        try:
            result = self.session.place_order(
                category="linear",
                symbol=instId,
                side=side,
                orderType=ordType,
                qty=sz,
                price=price,
                timeInForce="PostOnly",
                isLeverage=1,
            )
        except pybit.exceptions.FailedRequestError as e:
            print(f"Failed to get wallet balance: {e}")

        res={
            'msg':result['retMsg'],
            'code':str(result['retCode'])
        }
        return res
    
    #獲取所有未成交訂單
    def orderState(self,instId):
        print('Not yet')
        # result=None
        # try:
        #     result = session.get_open_orders(
        #     category="linear",
        #     symbol=instId,
        #     openOnly=1
        # )
        # except pybit.exceptions.FailedRequestError as e:
        #     print(f"Failed to get wallet balance: {e}")
        #     return result

        # res={
        #     'code':result['code'],
        #     'msg':result['msg']
        # }
        
        # result=result['data']
        # listOrder=[]
        # for order in result:
        #     temp={
        #         'instId':order['instId'],
        #         'ordId':order['ordId']
        #     }
        #     listOrder.append(temp)
        # res={
        #     'code':'0',
        #     'listOrder':listOrder
        # }
        # return res
    
    #要用 my.cancelOrder(my.orderState()['listOrder'])
    def cancelOrder(self,instId):
        result=None
        try:
            result = self.session.cancel_all_orders(
                category="linear",
                symbol=instId,
            )
        except pybit.exceptions.FailedRequestError as e:
            print(f"Failed to get wallet balance: {e}")

        res={
            'msg':result['retMsg'],
            'code':str(result['retCode'])
        }
        return res
        

if __name__=='__main__':
        my=mybybit()
        a=my.trade('BTCUSDT',"Buy","Limit","66000","0.1")
        print(a)