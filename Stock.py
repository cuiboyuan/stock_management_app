from typing import Dict, List, Union, Optional
from Stock_Market_Calculations import *
import csv
import datetime

NEGATIVE_ERROR_MSG = "Error. Negative value"
SELL_ERROR_MSG = "Error. The stock does not exist"
RECORD_ERROR_MSG = 'Error. Invalid name or price'
NEGATIVE_DEPOSIT_MSG = 'Error. Negative Deposit'
NAME_ERROR_MSG = 'Invalid name'


INFO_PCS_NUM = 7
HISTORY_PCS_NUM = 3

NAME = 0
PRICE_TODAY = 1
NUM_HOLD = 2
COST = 3
FLOATING_PROFIT = 5
TOTAL_PROFIT = 6
MARKET_PRICE = 4

DATE = 0
OPERATION = 1
NOTE = 2


def right_now() -> str:

    NOW = datetime.datetime.now()
    hour = NOW.hour
    minute = NOW.minute
    second = NOW.second
    if len(str(NOW.minute)) == 1:
        minute = '0' + str(NOW.minute)
    if len(str(NOW.hour)) == 1:
        hour = '0' + str(NOW.hour)
    if len(str(NOW.second)) == 1:
        second = '0' + str(NOW.second)
    TODAY = '{}-{}-{} {}:{}:{}'.format(NOW.year, NOW.month, NOW.day, hour, minute, second)
    return TODAY


class TotalAssets:

    def __init__(self, total_stocks: str, total_assets: str, history: str, name='default') -> None:

        self.name = name

        self._stocks = total_stocks
        self._asset_record = total_assets
        self._history_file = history
        try:
            f = open(total_assets, 'r', encoding='UTF-8-sig')
            self._deposits = float(f.readline())
            self.fund_movement = float(f.readline())
            self._service_fee_rate = float(f.readline())
            f.close()
        except TypeError:
            pass

    def get_stock_file(self) -> str:

        return self._stocks

    def get_asset_record(self) -> str:

        return self._asset_record

    def get_deposit(self) -> float:

        return self._deposits

    def get_history_file(self) -> str:

        return self._history_file

    def get_service_fee_rate(self) -> float:

        return self._service_fee_rate

    def edit_service_fee_rate(self, new: float) -> None:

        self._service_fee_rate = new
        w = open(self.get_asset_record(), 'w', newline='', encoding='UTF-8-sig')
        w.write(str(self.get_deposit()) + '\n' + str(self.fund_movement) + '\n' + str(self._service_fee_rate))
        w.close()

    def record_deposit_history(self, amount: float, note: str, income=True) -> None:

        a = open(self.get_history_file(), 'a', newline='', encoding='UTF-8-sig')
        history_write = csv.writer(a)
        content = ''

        updated_info = []
        for _ in range(3):
            updated_info.append('NA')

        updated_info[DATE] = right_now()

        if income:
            content = '存款{}元'.format(amount)
        else:
            content = '取款{}元'.format(amount)
        updated_info[OPERATION] = content
        updated_info[NOTE] = note

        history_write.writerow(updated_info)
        a.close()

    def record_stock_history(self, name: str, num: int, price: float, note: str, buy=True) -> None:

        a = open(self.get_history_file(), 'a', newline='', encoding='UTF-8-sig')
        history_write = csv.writer(a)
        content = ''

        updated_info = []
        for _ in range(3):
            updated_info.append('NA')

        updated_info[DATE] = right_now()

        if buy:
            content = '买入{} {}股，每股{}元'.format(name, num, price)
        else:
            content = '卖出{} {}股，每股{}元'.format(name, num, price)
        updated_info[OPERATION] = content
        updated_info[NOTE] = note

        history_write.writerow(updated_info)
        a.close()

    def record_price_history(self, name: str, price: float, note: str) -> None:

        a = open(self.get_history_file(), 'a', newline='', encoding='UTF-8-sig')
        history_write = csv.writer(a)

        updated_info = []
        for _ in range(3):
            updated_info.append('NA')

        updated_info[DATE] = right_now()

        content = '记录{} 市价为{}元'.format(name, price)
        updated_info[OPERATION] = content
        updated_info[NOTE] = note

        history_write.writerow(updated_info)
        a.close()

    def record_share_history(self, name: str, amount: Union[int, float], note: str, cash=True) -> None:

        a = open(self.get_history_file(), 'a', newline='', encoding='UTF-8-sig')
        history_write = csv.writer(a)
        content = ''

        updated_info = []
        for _ in range(3):
            updated_info.append('NA')

        updated_info[DATE] = right_now()

        if cash:
            content = '{} 分红利得到 {}元'.format(name, amount)
        else:
            content = '{} 分红股得到 {}股'.format(name, amount)
        updated_info[OPERATION] = content
        updated_info[NOTE] = note

        history_write.writerow(updated_info)
        a.close()

    def income(self, amount: float, note: str) -> Optional[str]:

        if amount < 0:
            print(NEGATIVE_ERROR_MSG)
            return NEGATIVE_ERROR_MSG
        self._deposits = round(self._deposits + amount, 2)
        self.fund_movement = round(self.fund_movement + amount, 2)

        w = open(self.get_asset_record(), 'w', newline='', encoding='UTF-8-sig')
        w.write(str(self.get_deposit()) + '\n' + str(self.fund_movement) + '\n' + str(self._service_fee_rate))
        w.close()

        self.record_deposit_history(amount, note)

    def expense(self, amount: float, note: str) -> Optional[str]:

        if amount < 0:
            print(NEGATIVE_ERROR_MSG)
            return NEGATIVE_ERROR_MSG
        if self.get_deposit() - amount < 0:
            return NEGATIVE_DEPOSIT_MSG
        self._deposits = round(self._deposits - amount, 2)
        self.fund_movement = round(self.fund_movement - amount, 2)

        w = open(self.get_asset_record(), 'w', newline='', encoding='UTF-8-sig')
        w.write(str(self.get_deposit()) + '\n' + str(self.fund_movement) + '\n' + str(self._service_fee_rate))
        w.close()

        self.record_deposit_history(amount, note, income=False)

    def stock_earn(self, amount: float) -> Optional[str]:

        if amount < 0:
            print(NEGATIVE_ERROR_MSG)
            return NEGATIVE_ERROR_MSG
        self._deposits = round(self._deposits + amount, 2)

        w = open(self.get_asset_record(), 'w', newline='', encoding='UTF-8-sig')
        w.write(str(self.get_deposit()) + '\n' + str(self.fund_movement) + '\n' + str(self._service_fee_rate))
        w.close()

    def stock_expense(self, amount: float) -> Optional[str]:

        if amount < 0:
            print(NEGATIVE_ERROR_MSG)
            return NEGATIVE_ERROR_MSG
        if self.get_deposit() - amount < 0:
            return NEGATIVE_DEPOSIT_MSG
        self._deposits = round(self._deposits - amount, 2)

        w = open(self.get_asset_record(), 'w', newline='', encoding='UTF-8-sig')
        w.write(str(self.get_deposit()) + '\n' + str(self.fund_movement) + '\n' + str(self._service_fee_rate))
        w.close()

    def change_stock_info(self, name, new_row: list) -> None:

        f = open(self.get_stock_file(), 'r', encoding='UTF-8-sig')
        stock_read = csv.reader(f)

        new_file = []
        for line in stock_read:
            if line[NAME] == '':
                continue
            if name == line[NAME]:
                new_file.append(new_row)
                continue
            new_file.append(line)
        f.close()

        w = open(self.get_stock_file(), 'w', newline='', encoding='UTF-8-sig')
        stock_write = csv.writer(w)
        for line in new_file:
            stock_write.writerow(line)
        w.close()

    def add_new_stock(self, name: str, price: float, num_bought: int) -> None:

        a = open(self.get_stock_file(), 'a', newline='', encoding='UTF-8-sig')
        stock_write = csv.writer(a)

        updated_info = []
        for _ in range(INFO_PCS_NUM):
            updated_info.append('NA')

        updated_info[NAME] = name
        # updated_info[CODE] = code
        updated_info[PRICE_TODAY] = round(price, 2)
        updated_info[NUM_HOLD] = num_bought

        new_cost = round(price * (1 + self._service_fee_rate), 2)
        new_profit = get_floating_profit(price, new_cost, num_bought)

        updated_info[COST] = new_cost
        updated_info[FLOATING_PROFIT] = new_profit
        updated_info[TOTAL_PROFIT] = new_profit
        updated_info[MARKET_PRICE] = str(get_market_price(price, num_bought))

        stock_write.writerow(updated_info)
        a.close()

    def sell_stock(self, name: str, num_sold: int, price: float, note: str) -> Optional[str]:

        stock_exists = False
        deposit_msg = None
        f = open(self.get_stock_file(), 'r', encoding='UTF-8-sig')
        stock_read = csv.reader(f)

        updated_info = []
        for _ in range(INFO_PCS_NUM):
            updated_info.append('NA')

        f.readline()

        for stock in stock_read:
            if stock[NAME] == name:
                deposit_msg = self.stock_earn(price * num_sold * (1 - self._service_fee_rate))

                new_num_hold = int(stock[NUM_HOLD]) - num_sold
                new_price = round(price,2)

                new_cost = get_cost(price * (1 - self._service_fee_rate), stock[COST], stock[NUM_HOLD],
                                    -num_sold)
                new_float_profit = get_floating_profit(new_price, new_cost,
                                                       new_num_hold)
                sellout_float_profit = get_floating_profit(price, stock[COST], stock[NUM_HOLD])
                if new_float_profit == 'NA':
                    new_total = float(stock[TOTAL_PROFIT]) - float(stock[
                        FLOATING_PROFIT]) + sellout_float_profit
                else:
                    new_total = float(stock[TOTAL_PROFIT]) - float(stock[
                        FLOATING_PROFIT]) + new_float_profit

                updated_info[NAME] = stock[NAME]
                # updated_info[CODE] = stock[CODE]
                updated_info[PRICE_TODAY] = str(new_price)
                updated_info[NUM_HOLD] = str(new_num_hold)
                updated_info[COST] = str(new_cost)
                updated_info[FLOATING_PROFIT] = str(new_float_profit)
                updated_info[TOTAL_PROFIT] = str(new_total)
                updated_info[MARKET_PRICE] = str(
                    get_market_price(new_price, new_num_hold))

                if new_num_hold >= 0:
                    stock_exists = True
                break
        f.close()

        if stock_exists:
            self.change_stock_info(name, updated_info)
            self.record_stock_history(name, num_sold, price, note, buy=False)
        else:
            if deposit_msg is not None:
                return deposit_msg
            print(SELL_ERROR_MSG)
            return SELL_ERROR_MSG

    def buy_stock(self, name: str, num_bought: int, price: float,
                  note: str) -> Optional[str]:

        new_stock = True
        f = open(self.get_stock_file(), 'r', encoding='UTF-8-sig')
        stock_read = csv.reader(f)

        deposit_msg = self.stock_expense(round(price * num_bought * (1 + self._service_fee_rate), 2))

        updated_info = []
        for _ in range(INFO_PCS_NUM):
            updated_info.append('NA')

        f.readline()

        for stock in stock_read:
            if stock[NAME] == name:
                new_num_hold = int(stock[NUM_HOLD]) + num_bought
                new_price = round(price,2)
                if stock[COST] == 'NA':
                    new_cost = round(price * (1 + self._service_fee_rate), 2)
                else:

                    new_cost = get_cost(price * (1 + self._service_fee_rate), stock[COST],
                                        stock[NUM_HOLD], num_bought)
                new_float_profit = get_floating_profit(new_price, new_cost,
                                                       new_num_hold)
                if new_float_profit == 'NA':
                    new_total = float(stock[TOTAL_PROFIT])
                elif stock[FLOATING_PROFIT] == 'NA':
                    new_total = float(stock[TOTAL_PROFIT]) + new_float_profit
                else:
                    new_total = float(stock[TOTAL_PROFIT]) - float(stock[
                        FLOATING_PROFIT]) + new_float_profit

                updated_info[NAME] = stock[NAME]
                # updated_info[CODE] = stock[CODE]
                updated_info[PRICE_TODAY] = str(new_price)
                updated_info[NUM_HOLD] = str(new_num_hold)
                updated_info[COST] = str(new_cost)
                updated_info[FLOATING_PROFIT] = str(new_float_profit)
                updated_info[TOTAL_PROFIT] = str(new_total)
                updated_info[MARKET_PRICE] = str(
                    get_market_price(new_price, new_num_hold))

                new_stock = False
                break
        f.close()

        if deposit_msg is not None:
            return deposit_msg

        if new_stock:
            self.add_new_stock(name, price, num_bought)
        else:
            self.change_stock_info(name, updated_info)

        self.record_stock_history(name, num_bought, price, note)

    def record_price_today(self, name: str, price_now: float, note: str) -> Optional[str]:

        stock_exists = False
        f = open(self.get_stock_file(), 'r', encoding='UTF-8-sig')
        stock_read = csv.reader(f)

        updated_info = []
        for _ in range(INFO_PCS_NUM):
            updated_info.append('NA')

        f.readline()

        for stock in stock_read:
            if name == '' or price_now <= 0:
                return RECORD_ERROR_MSG
            if stock[NAME] == name:

                if stock[COST] == 'NA':
                    new_float_profit = 'NA'
                else:
                    new_float_profit = get_floating_profit(price_now,
                                                       float(stock[COST]),
                                                       int(stock[NUM_HOLD]))

                updated_info[NAME] = stock[NAME]
                # updated_info[CODE] = stock[CODE]
                updated_info[PRICE_TODAY] = str(round(price_now,2))
                updated_info[NUM_HOLD] = stock[NUM_HOLD]
                updated_info[COST] = stock[COST]
                updated_info[FLOATING_PROFIT] = str(new_float_profit)
                if stock[FLOATING_PROFIT] == 'NA':
                    updated_info[TOTAL_PROFIT] = stock[TOTAL_PROFIT]
                else:
                    updated_info[TOTAL_PROFIT] = float(stock[TOTAL_PROFIT]) - float(stock[FLOATING_PROFIT]) + new_float_profit
                updated_info[MARKET_PRICE] = str(
                    get_market_price(price_now, int(stock[NUM_HOLD])))

                stock_exists = True
                break
        f.close()

        if stock_exists:
            self.change_stock_info(name, updated_info)
            self.record_price_history(name, price_now, note)
        else:
            return SELL_ERROR_MSG

    def give_share(self, name: str, share_rate: float, note: str, cash_share=True) -> Optional[str]:

        stock_exists = False
        f = open(self.get_stock_file(), 'r', encoding='UTF-8-sig')
        stock_read = csv.reader(f)

        updated_info = []
        for _ in range(INFO_PCS_NUM):
            updated_info.append('NA')

        f.readline()

        for stock in stock_read:
            if name == '':
                return NAME_ERROR_MSG
            if share_rate < 0:
                return NEGATIVE_ERROR_MSG
            if stock[NAME] == name:

                if cash_share:
                    new_cost = float(stock[COST]) - share_rate
                    new_hold = int(stock[NUM_HOLD])
                    self.income(round(int(stock[NUM_HOLD])*share_rate, 2), note)
                else:
                    new_hold = round(int(stock[NUM_HOLD]) *(1 + share_rate))
                    new_cost = get_cost(0, stock[COST], stock[NUM_HOLD], round(int(stock[NUM_HOLD])*share_rate))


                new_float_profit = get_floating_profit(stock[PRICE_TODAY],
                                                       new_cost,
                                                       int(stock[NUM_HOLD]))
                new_total_profit = float(stock[TOTAL_PROFIT]) - float(
                    stock[FLOATING_PROFIT]) + new_float_profit

                updated_info[NAME] = stock[NAME]
                # updated_info[CODE] = stock[CODE]
                updated_info[PRICE_TODAY] = stock[PRICE_TODAY]
                updated_info[NUM_HOLD] = new_hold
                updated_info[COST] = round(new_cost,2)
                updated_info[FLOATING_PROFIT] = new_float_profit
                updated_info[TOTAL_PROFIT] = new_total_profit
                updated_info[MARKET_PRICE] = new_hold * float(stock[PRICE_TODAY])
                stock_exists = True

                amount_cash = round(int(stock[NUM_HOLD])*share_rate, 2)
                amount_stock = round(int(stock[NUM_HOLD]) * (share_rate),2)
                if cash_share:
                    self.record_share_history(name, amount_cash, note)
                else:
                    self.record_share_history(name, amount_stock, note, cash=False)

                break
        f.close()

        if stock_exists:
            self.change_stock_info(name, updated_info)
        else:
            return SELL_ERROR_MSG

    def clear_all(self) -> None:

        f = open(self.get_stock_file(), 'r', encoding='UTF-8-sig')
        header = f.readline().split(sep=',')
        header[-1] = header[-1].strip()
        # print(header)
        f.close()

        w = open(self.get_stock_file(), 'w', newline='', encoding='UTF-8-sig')
        csv_write = csv.writer(w)
        csv_write.writerow(header)
        w.close()

        a = open(self.get_asset_record(), 'w', newline='', encoding='UTF-8-sig')
        a.write('0.00\n0.00\n0.001')
        self._deposits = 0
        self.fund_movement = 0
        self._service_fee_rate = 0.001
        a.close()

        h_f = open(self.get_history_file(), 'r', encoding='UTF-8-sig')
        header = h_f.readline().split(sep=',')
        header[-1] = header[-1].strip()
        # print(header)
        h_f.close()

        h_w = open(self.get_history_file(), 'w', newline='', encoding='UTF-8-sig')
        csv_write = csv.writer(h_w)
        csv_write.writerow(header)
        h_w.close()


if __name__ == '__main__':

    CSV_NAME = 'New Microsoft Excel Worksheet.csv'
    TXT_NAME = 'New Text Document.txt'
    HISTORY_NAME = 'History.csv'

    a = TotalAssets(CSV_NAME, TXT_NAME, HISTORY_NAME)
    a.clear_all()
