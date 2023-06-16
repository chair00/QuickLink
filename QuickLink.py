from flask import Flask, render_template, request, redirect
import string
import random
import validators


quicklink = Flask(__name__)

class URLShortener:
    def __init__(self):
        self.urls = {}
    
    def shorten_url(self, long_url):
        characters = string.ascii_letters + string.digits
        short_url = ''.join(random.choice(characters) for _ in range(6))
        self.urls[short_url] = long_url
        return short_url
    
    def get_long_url(self, short_url):
        return self.urls.get(short_url)

class URLStorage:
    def __init__(self):
        self.url_shortener = URLShortener()
    
    def add_url(self, long_url):
        return self.url_shortener.shorten_url(long_url)
    
    def get_long_url(self, short_url):
        return self.url_shortener.get_long_url(short_url)


class URLValidator:
    def validate_url(self, url):
        return validators.url(url)


class RequestHandler:
    def __init__(self):
        self.url_storage = URLStorage()
        self.url_validator = URLValidator()
    
    def handle_shorten_request(self, long_url):
        if self.url_validator.validate_url(long_url):
            short_url = self.url_storage.add_url(long_url)
            return short_url
        return None
    
    def handle_redirect_request(self, short_url):
        long_url = self.url_storage.get_long_url(short_url)
        return long_url

request_handler = RequestHandler()

@quicklink.route('/')
def home():
    return render_template('index.html')

@quicklink.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form.get('url')

    # Check if the URL starts with 'http://' or 'https://'
    if not long_url.startswith('http://') and not long_url.startswith('https://'):
        long_url = 'http://' + long_url  # Add 'http://' prefix to the URL

    # Check if the URL starts with 'www.'
    if long_url.startswith('www.'):
        long_url = 'http://' + long_url  # Add 'http://' prefix to the URL

    short_url = request_handler.handle_shorten_request(long_url)
    if short_url:
        return render_template('result.html', short_url=short_url)
    else:
        return render_template('invalid.html')



@quicklink.route('/<short_url>')
def redirect_to_long_url(short_url):
    long_url = request_handler.handle_redirect_request(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return render_template('invalid.html')

if __name__ == '__main__':
    quicklink.run()
