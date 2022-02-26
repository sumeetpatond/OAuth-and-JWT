ROOT_URL = 'https://openexchangerates.org/api'

COMMON_URL_PARAM = '?app_id=9ca09d09f30d4613a1cf2e5b126f3399'
# .format(os.environ.get("EXCHANGE_API_KEY"))

LATEST_URL = ROOT_URL + '/latest.json' + COMMON_URL_PARAM
HISTORICAL_URL = ROOT_URL + '/historical/{}.json' + COMMON_URL_PARAM
CURRENCY_URL = ROOT_URL + '/currencies.json' + COMMON_URL_PARAM
COVERT_URL = ROOT_URL + '/convert' + COMMON_URL_PARAM
