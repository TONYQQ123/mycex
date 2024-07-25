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
        self.um_futures_client = UMFutures(key=key, secret=secret,base_url=self.url)
    

    def balance(self, ccy, recvWindow=6000):
        try:
            response = self.um_futures_client.balance(recvWindow=recvWindow)
            return {
                'code': '0',
                'msg': '',
                'response': response
            }
        except ClientError as error:
            return {
                'code': '1',
                'msg': f"Error fetching balance: {error.status_code}, {error.error_code}, {error.error_message}"
            }
    
    def position(self):
        try:
            response = self.um_futures_client.position()
            return {
                'code': '0',
                'msg': '',
                'response': response
            }
        except ClientError as error:
            return {
                'code': '1',
                'msg': f"Error fetching position: {error.status_code}, {error.error_code}, {error.error_message}"
            }
    
    def fundingRatio(self, instId, recvWindow=6000):
        try:
            response = self.um_futures_client.funding_rate(instId, recvWindow=recvWindow)
            return {
                'code': '0',
                'msg': '',
                'response': response
            }
        except ClientError as error:
            return {
                'code': '1',
                'msg': f"Error fetching funding rate: {error.status_code}, {error.error_code}, {error.error_message}"
            }
    
    def price(self, instId):
        try:
            response = self.um_futures_client.ticker_price(instId)
            return {
                'code': '0',
                'msg': '',
                'response': response
            }
        except ClientError as error:
            return {
                'code': '1',
                'msg': f"Error fetching price: {error.status_code}, {error.error_code}, {error.error_message}"
            }
    
    def bianceTime(self):
        try:
            response = self.um_futures_client.time()
            return {
                'code': '0',
                'msg': '',
                'response': response
            }
        except ClientError as error:
            return {
                'code': '1',
                'msg': f"Error fetching server time: {error.status_code}, {error.error_code}, {error.error_message}"
            }
    
    def trade(self, instId, side, ordType, price, sz, recvWindow=5000):
        try:
            response = self.um_futures_client.new_order(
                symbol=instId,
                side=side,
                type=ordType,
                quantity=sz,
                price=price,
                recvWindow=recvWindow
            )
            return {
                'code': '0',
                'msg': '',
                'response': response
            }
        except ClientError as error:
            return {
                'code': '1',
                'msg': f"Error placing order: {error.status_code}, {error.error_code}, {error.error_message}"
            }
    
     def orderState(self, orderId, origClientOrderId=None, recvWindow=5000):
        try:
            response = self.um_futures_client.get_order(
                symbol=instId,
                orderId=orderId,
                origClientOrderId=origClientOrderId,
                recvWindow=recvWindow
            )
            return {
                'code': '0',
                'msg': '',
                'response': response
            }
        except ClientError as error:
            return {
                'code': '1',
                'msg': f"Error fetching order state: {error.status_code}, {error.error_code}, {error.error_message}"
            }
    
    def cancelOrder(self, symbol, orderId=None, origClientOrderId=None, recvWindow=2000):
        try:
            response = self.um_futures_client.cancel_order(
                symbol=symbol,
                orderId=orderId,
                origClientOrderId=origClientOrderId,
                recvWindow=recvWindow
            )
            return {
                'code': '0',
                'msg': '',
                'response': response
            }
        except ClientError as error:
            return {
                'code': '1',
                'msg': f"Error cancelling order: {error.status_code}, {error.error_code}, {error.error_message}"
            }

if __name__ == '__main__':
    # 示例用法，您可以在此处测试调用这些函数
    my_binance = mybiance()
    print(my_binance.balance("BTC"))
    print(my_binance.position())
    print(my_binance.fundingRatio("BTCUSDT"))
    print(my_binance.price("BTCUSDT"))
    print(my_binance.bianceTime())
    print(my_binance.trade("BTCUSDT", "BUY", "LIMIT", 60000, 1))
    print(my_binance.orderState("BTCUSDT", orderId="12345"))
    print(my_binance.cancelOrder("BTCUSDT", orderId="12345"))
