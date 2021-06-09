from contextlib import contextmanager
from selenium import webdriver


@contextmanager
def get_driver():
    try:
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.binary_location = '/opt/chrome'
        driver = webdriver.Chrome(executable_path='/opt/chromedriver',
                                  options=chrome_options)
        yield driver
    finally:
        driver.quit()


def get_quote(symbol):
    print('Executing... It works')
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.binary_location = '/opt/chrome'
    driver = webdriver.Chrome(executable_path='/opt/chromedriver',
                                  options=chrome_options)
    driver.get(f"https://www.reuters.com/companies/{symbol}.SA")
    data = {}
    data['symbol'] = symbol
    data['price'] = driver.find_element_by_css_selector(
        '#__next > div > div.TwoColumnsLayout-hero-3H8pu > div > div > div > div.QuoteRibbon-price-Byg3o > span.TextLabel__text-label___3oCVw.TextLabel__black___2FN-Z.TextLabel__light___1WILL.digits.last.QuoteRibbon-digits-30Sds'
    ).text

    return data


def handler(env, context):
    print(get_quote('TAEE11'))
