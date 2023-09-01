from enum import Enum


class OperationTypeEnum(Enum):
    add = 'add'
    update = 'update'
    disable = 'disable'
    stopSell = 'stopSell'
    startSell = 'startSell'


class HistoryOrderUpdateEnum(Enum):
    history = 'history'


class CategoryEnum(Enum):

    credit = 'credit'  # 信用账户
    shares = 'shares'  # 股票账户

# 中信委托类型
# class TradeSide(Enum):
#
#     BUY = '1'
#     MARGIN_BUY = 'A'
#     DEBIT_BUY = 'C'
#     SELL = '2'
#     MARGIN_SELL = 'B'
#     DEBIT_SELL = 'D'

# 中金委托类型
class TradeSide(Enum):

    BUY = '23'
    MARGIN_BUY = '27'
    DEBIT_BUY = '29'
    SELL = '24'
    MARGIN_SELL = '28'
    DEBIT_SELL = '31'

# 中信报价类型
# class PriceType(Enum):
#     STOCK_LIMIT = '0'

# 中金报价类型
class PriceType(Enum):
    STOCK_LIMIT = '11'

if __name__ == '__main__':
    side = TradeSide('1')
    print(side)
    side2 = TradeSide['BUY']
    print(side2)
