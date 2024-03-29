from app.v1.coin.model.CoinModel import CoinModel
from tuuz.Calc import Bc


class CoinCalcAction:
    Coin: {} = None
    coin_id = 0
    __price4one = 0

    def __init__(self, coin_id):
        self.coin_id = coin_id
        self.Coin = CoinModel().api_find(coin_id)
        if not self.Coin:
            raise Exception("没有找到对应的币")

    def _price_for_one_token(self):
        if self.Coin is None:
            return None
        price = self.Coin["price"]
        token = self.Coin["token"]
        self.__price4one = Bc.div(price, token)

    def Calc(self, amount):
        if self.Coin is None:
            return None
        final_amount = Bc.mul(amount, self.__price4one)
        return final_amount
