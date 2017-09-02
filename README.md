<h1>Glavpetuh Telegram Bot</h1>

Simple telegram bot built with python using [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library

## Installation

First clone this repo:

    git clone https://github.com/Spirokky/glavpetuh.git
    cd glavpetuh

Configure your virtual environment and install all requirements using`requirements.txt`:

    virtualenv env
	pip install -r requirements.txt

Install [Node.js](https://nodejs.org/en/) and download [PhantomJS](http://phantomjs.org/download.html).

Edit `src/config/config.py` , make sure `webdriver_path` variable is correct path to your PhantomJS driver.

Create `src/config/secrets.py` with secret variable `TOKEN`

Run bot:

    cd src/
    python bot.py

