import requests
import pandas

ZETA_VALLEY_URL='http://127.0.0.1:3000'

def format_output(data):
    if isinstance(data, list):
        # If the call returns a list, then we will append them
        # in the resulting data frame. If in the future
        # alphavantage decides to do more with returning arrays
        # this might become buggy. For now will do the trick.
        if not data:
            data_pandas = pandas.DataFrame()
        else:
            data_array = []
            for val in data:
                data_array.append([v for _, v in val.items()])
            data_pandas = pandas.DataFrame(data_array, columns=[
                k for k, _ in data[0].items()])
    else:
        data_pandas = pandas.DataFrame.from_dict(data,
                                                 orient='index',
                                                 dtype='float')
    
    return data_pandas

def get_balance_sheet_annual(ticker):
    url = f'{ZETA_VALLEY_URL}/{ticker}/balancesheet'
    req = requests.get(url)

    if req.status_code != 200:
        raise Exception('Zeta Valley Error')

    data = req.json()
    annualReports = data['annualReports']
    return (format_output(annualReports), ticker)

def get_income_statement_annual(ticker):
    url = f'{ZETA_VALLEY_URL}/{ticker}/incomestatement'
    req = requests.get(url)

    if req.status_code != 200:
        raise Exception('Zeta Valley Error')

    data = req.json()
    annualReports = data['annualReports']
    return (format_output(annualReports), ticker)

def get_cash_flow_annual(ticker):
    url = f'{ZETA_VALLEY_URL}/{ticker}/cashflow'
    req = requests.get(url)

    if req.status_code != 200:
        raise Exception('Zeta Valley Error')

    data = req.json()
    annualReports = data['annualReports']
    return (format_output(annualReports), ticker)

if __name__ == '__main__':
    # import os
    # from alpha_vantage.fundamentaldata import FundamentalData
    # Load environment variables
    # from dotenv import load_dotenv
    # load_dotenv()

    # alpha_vantage_key = os.getenv('ALPHA_VANTAGE_KEY')

    # fd = FundamentalData(key=alpha_vantage_key, output_format='pandas')
    # balance_sheet = fd.get_balance_sheet_annual('TLSA')

    # print(balance_sheet)
    # print(balance_sheet[0])

    print(get_income_statement_annual('TSLA'))