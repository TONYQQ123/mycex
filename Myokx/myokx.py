import okx.Account as Account
import okx.PublicData as PublicData
import okx.Trade as Trade
import json

class myokx():
    def __init__(self):
        with open('okxConfi.json') as f:
            confi=json.load(f)

        apikey = confi['api_key']
        secretkey = confi['secretkey']
        passphrase = confi['passphrase']
        flag=confi['flag']
        self.accountAPI = Account.AccountAPI(apikey, secretkey, passphrase, False, flag)
        self.dataAPI = PublicData.PublicAPI(flag=flag)
        self.tradeAPI = Trade.TradeAPI(apikey, secretkey, passphrase, False, flag)
    #usdt usdc用avabal可用餘額
    def balance(self,ccy):
        result=self.accountAPI.get_account_balance()

        if result['code']!='0':
            res={
                'msg':result['msg']
            }
            return res

        result=result['data'][0]
        total=result.get('totalEq')
        detail=result.get('details')
        USDT_ava='0'
        USDC_ava='0'
        #breakpoint()
        target='0'
        for data in detail:
            if data.get('ccy')==ccy:
                target=data.get('cashBal','0')
            if data.get('ccy')=='USDT':
                USDT_ava=data.get('availBal','0')
            if data.get('ccy')=='USDC':
                USDC_ava=data.get('availBal','0')
        res={
            'total':total,
            'USDT':USDT_ava,
            'USDC':USDC_ava,
            ccy:target
        }
        return res
    
    def position(self):
        result=self.accountAPI.get_positions(instType='SWAP')

        if result['code']!='0':
            res={
                'msg':result['msg']
            }
            return res

        result=result.get('data')
        res={
            'pos':[]
        }
        for data in result:
            temp={}
            temp['ccy']=data.get('instId')
            temp['id']=data.get('posId')
            temp['num']=data.get('pos')
            temp['avgprice']=data.get('avgPx')
            temp['gain']=data.get('upl')
            temp['gainRatio']=data.get('uplRatio')
            temp['closed']=data.get('liqPx')#強平價
            temp['margin']=data.get('margin')#保證金
            temp['fee']=data.get('fee')#累計手續費
            temp['fundingFee']=data.get('fundingFee')#累計資金費
            res['pos'].append(temp)
        return res
    
    def setLever(self,instId,lever):
        result = self.accountAPI.set_leverage(
            instId=instId,
            lever=lever,
            mgnMode="isolated"
        )
        res={
            'code':result['code'],
            'msg':result['msg']
        }
        return res
    
    #若 settState = processing，
    #该字段代表用于本轮结算的资金费率；若 settState = settled，
    #该字段代表用于上轮结算的资金费率
    def fundingRatio(self,instId):
        result = self.dataAPI.get_funding_rate(
        instId=instId,
        )

        if result['code']!='0':
            res={
                'msg':result['msg']
            }
            return res

        result=result['data'][0]
        res={}
        res['ratio']=result['fundingRate']
        res['nextTime']=result['nextFundingTime']
        res['state']=result['settState']
        res['settFundingRate']=result['settFundingRate']
        if result['method']=='next_period':
            res['ratio']=result['nextFundingRate']
        
        return res
    
    def price(self,instId):
        result = self.dataAPI.get_price_limit(
            instId=instId,
        )
        
        if result['code']!='0':
            res={
                'msg':result['msg']
            }
            return res
        result=result['data'][0]
        if not result['enabled']:
            res={
                'msg':'enable=false'
            }
            return res

        res={
            'minSell':result['sellLmt'],
        }
        return res
    
    def okxTime(self):
        result = self.dataAPI.get_system_time()
        if result['code']!='0':
            res={
                'msg':result['msg']
            }
            return res
        result=result['data'][0]['ts']
        return result

    #交易 mode:isolated：逐仓 ；cross：全仓
    #非保证金模式：cash
    #單位要修改sz

    def trade(self,instId,mode,side,ordType,price,sz):
        result=None
        if ordType=='limit':
            result = self.tradeAPI.place_order(
            instId=instId,
            tdMode=mode,
            side=side,
            ordType='limit',
            px=price,
            sz=sz
            )
        else:
            result = self.tradeAPI.place_order(
            instId=instId,
            tdMode=mode,
            side=side,
            ordType='market',
            sz=sz
            )

        if result['code']!='0':
            res={
                'code':result['code'],
                'msg':result['msg']
            }
            return res

        res={
            'code':result['code'],
            'id':result['data'][0]['ordId']
        }
        return res
    
    #獲取所有未成交訂單
    def orderState(self):
        result = self.tradeAPI.get_order_list()
        if result['code']!='0':
            res={
                'code':result['code'],
                'msg':result['msg']
            }
            return res
        result=result['data']
        listOrder=[]
        for order in result:
            temp={
                'instId':order['instId'],
                'ordId':order['ordId']
            }
            listOrder.append(temp)
        res={
            'code':'0',
            'listOrder':listOrder
        }
        return res
    
    #要用 my.cancelOrder(my.orderState()['listOrder'])
    def cancelOrder(self,listOrder):
        result = self.tradeAPI.cancel_multiple_orders(listOrder)
        if result['code']!='0':
            res={
                'code':result['code'],
                'msg':result['msg']
            }
        res={
            'code':'0'
        }
        return res
        

if __name__=='__main__':
        my=myokx()
        l=my.orderState()
        print(l['listOrder'])
        print(my.cancelOrder(l['listOrder']))