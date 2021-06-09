from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.headless = True  # also works
    driver = webdriver.Chrome(executable_path='/Users/jorgecorradi/Downloads/chromedriver', options=chrome_options)
    driver.get('https://www.infomoney.com.br/cotacoes/empresas-b3/')

    symbols = []
    for el in driver.find_elements_by_css_selector('.list-companies a'):
        symbols.append(el.text)

    with open('/Users/jorgecorradi/Desktop/stocks.csv', 'w') as csv_file:
        csv_file.write("symbol;companyName;stockType;sector;category;currency" + "\n")
        for symbol in symbols:
            driver.get('https://www.fundamentus.com.br/detalhes.php?papel=' + symbol)
            print("Scraping " + symbol)

            try:
                data = {}
                data['"symbol"'] = symbol

                type = driver.find_element_by_css_selector(
                    'body > div.center > div.conteudo.clearfix > table:nth-child(2) > tbody > tr:nth-child(1) > td.label.w15 > span.txt').text

                if type == 'Papel':
                    data['companyName'] = driver.find_element_by_css_selector(
                        'body > div.center > div.conteudo.clearfix > table:nth-child(2) > tbody > tr:nth-child(3) > td:nth-child(2) > span').text

                    data['stockType'] = driver.find_element_by_css_selector(
                        'body > div.center > div.conteudo.clearfix > table:nth-child(2) > tbody > tr:nth-child(2) > td:nth-child(2) > span').text
                    data['sector'] = driver.find_element_by_css_selector(
                        'body > div.center > div.conteudo.clearfix > table:nth-child(2) > tbody > tr:nth-child(4) > td:nth-child(2) > span > a').text
                    data['category'] = 'STOCK'
                else:
                    data['companyName'] = driver.find_element_by_css_selector(
                        'body > div.center > div.conteudo.clearfix > table:nth-child(3) > tbody > tr:nth-child(2) > td:nth-child(2) > span').text

                    data['stockType'] = 'FII'
                    data['sector'] = driver.find_element_by_css_selector(
                        'body > div.center > div.conteudo.clearfix > table:nth-child(3) > tbody > tr:nth-child(4) > td:nth-child(2) > span > a').text
                    data['category'] = 'REF'

                data['currency'] = 'BRL'

                csv_file.write(";".join(data.values()) + "\n")
                csv_file.flush()
            except:
                print("couldn't get info for " + symbol)


if __name__ == '__main__':
    main()
    print("Done Scraping")
