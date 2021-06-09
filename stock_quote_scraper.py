import time

from flask import Flask, jsonify
from selenium import webdriver

app = Flask(__name__)


@app.route('/quote/<symbol>', methods=['GET'])
def scrape(symbol):
    driver = webdriver.chrome('/Users/jorgecorradi/devenv/chromedriver')
    driver.get('http://www.google.com/');
    time.sleep(5)  # Let the user actually see something!
    search_box = driver.find_element_by_name('q')
    search_box.send_keys('ChromeDriver')
    search_box.submit()
    time.sleep(5)  # Let the user actually see something!
    driver.quit()

    quote = {
        'symbol': symbol,
        'last_price': 0.12
    }
    return jsonify(quote), 200


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
