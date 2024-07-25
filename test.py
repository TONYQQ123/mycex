import requests
import time
import hashlib
import hmac
import base64
import urllib.parse
import json

class mybiance():
    def __init__(self):
        with open('bianceConfi.json') as f:
            confi=json.load(f)

        self.apikey = confi['api_key']
        self.secretkey = confi['secretkey']
        flag=confi['flag']
        if flag=='1':
            self.url='https://testnet.binancefuture.com'
        else:
            self.url='https://fapi.binance.com'
    
    def generate_signature(self, params):
        query_string = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
        signature = hmac.new(self.secretkey.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).digest()
        return urllib.parse.quote(base64.b64encode(signature))


    def balance(self,ccy):
        pass
    
    def position(self):
        pass
    

    def fundingRatio(self,instId):
        url=self.url+'/fapi/v1/premiumIndex'
        params={
            'symbol':instId
        }
        res={}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  
            data = response.json()
            res["markPrice"] = data["markPrice"]
            res[ "ratio"]=data[ "lastFundingRate"]
            res['nextTime']=data["nextFundingTime"]
            res['code']='0'
            res['msg']=''
            return res

        except requests.exceptions.RequestException as e:
            res['code']='1'
            res['msg']=e
            return res
    
    def price(self,instId):
        url=self.url+'/fapi/v1/ticker/price'
        params = {
        'symbol': instId
        }

        res={}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status() 
            data = response.json()
            res['price'] = data['price']
            res['code']='0'
            res['msg']=''
            return res

        except requests.exceptions.RequestException as e:
            res['code']='1'
            res['msg']=e
            return res
    
    def bianceTime(self):
        url=self.url+'/fapi/v1/time'
        res={}
        try:
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json()
            res['server_time'] = data['serverTime']
            res['code']='0'
            res['msg']=''
            return res

        except requests.exceptions.RequestException as e:
            res['code']='1'
            res['msg']=e
            return res

    def trade(self, instId, side, ordType, price, sz):
        url = self.url + '/fapi/v1/order'
        timestamp = int(time.time() * 1000)
        params = {
            'symbol': instId,
            'side': side,
            'type': ordType,
            'quantity': sz,
            'timestamp': timestamp,
            'recvWindow': 5000  
        }
        headers = {
            'Content-Type': 'application/json',
            'X-MBX-APIKEY': self.apikey,
        }
        try:
            signature = self.generate_signature(params)
            params['signature'] = signature
            response = requests.post(url, headers=headers, params=params)
            response.raise_for_status()
            print(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error placing order: {e}")
            breakpoint()

    def orderState(self):
        pass

    def cancelOrder(self,listOrder):
        pass
        

if __name__=='__main__':
        my=mybiance()
        print(my.trade('BTCUSDT','BUY','LIMIT',66000,1))