from typing import Union


def get_floating_profit(price: float, cost: Union[float, str],
                        num_hold: int) -> Union[float, str]:
    if cost == 'NA':
        return 'NA'
    return round((float(price) - float(cost)) * int(num_hold),2)


def get_cost(price: float, cost: float, num_hold: int,
             num_add: int) -> Union[float, str]:
    if int(num_hold) + int(num_add) <= 0:
        return 'NA'
    else:
        return round((float(cost) * int(num_hold) + float(price) * int(num_add)) / (
                int(num_hold) + int(num_add)),2)


def get_profit_or_loss(price: float, cost: float,
                       num_hold: int) -> float:
    return (price - cost) * num_hold


def get_market_price(price_now: float, num_hold: int) -> float:
    return round(float(price_now) * int(num_hold),2)


def convert_float_to_comma_sep_number(input: float) -> str:

    result = ''
    real_result = ''
    encountered_dot = False
    num_thousand = 0

    input_string = str(float(input))
    for i in range(len(input_string)-1, -1, -1):
        if num_thousand == 3:
            if input_string[i] == '-':
                pass
            else:
                result += ','
            num_thousand = 0

        if encountered_dot:
            num_thousand += 1

        if input_string[i] == '.':
            encountered_dot = True
        result += input_string[i]

    for i in range(len(result)-1, -1, -1):
        real_result += result[i]

    return real_result


if __name__ == '__main__':
    print(convert_float_to_comma_sep_number(3452344.34))
