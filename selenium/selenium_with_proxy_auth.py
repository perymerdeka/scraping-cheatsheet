import os
import random
import zipfile

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_driver(use_proxy=False, user_agent: list = None, ip_proxy: str = None, port: str = None, username: str = None,
               password: str = None):
    """Selenium setup"""
    options = Options()

    if use_proxy:
        print(f'Using Proxy: {ip_proxy}:{port}')
        try:
            os.mkdir('temp/plugins')
        except FileExistsError:
            pass

        manifest_json = """
                       {
                           "version": "1.0.0",
                           "manifest_version": 2,
                           "name": "Chrome Proxy",
                           "permissions": [
                               "proxy",
                               "tabs",
                               "unlimitedStorage",
                               "storage",
                               "<all_urls>",
                               "webRequest",
                               "webRequestBlocking"
                           ],
                           "background": {
                               "scripts": ["background.js"]
                           },
                           "minimum_chrome_version":"22.0.0"
                       }
                       """

        background_js = """
                       var config = {
                               mode: "fixed_servers",
                               rules: {
                               singleProxy: {
                                   scheme: "http",
                                   host: "%s",
                                   port: parseInt(%s)
                               },
                               bypassList: ["localhost"]
                               }
                           };
                           chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                       function callbackFn(details) {
                           return {
                               authCredentials: {
                                   username: "%s",
                                   password: "%s"
                               }
                           };
                       }

                       chrome.webRequest.onAuthRequired.addListener(
                                   callbackFn,
                                   {urls: ["<all_urls>"]},
                                   ['blocking']
                       );
                       """ % (ip_proxy, port, username, password)

        plugin_file = 'temp/plugins/proxy_auth.zip'
        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        options.extensions(plugin_file)
        options.add_argument(argument=f'argument={random.choice(user_agent)}')
        driver = webdriver.Chrome(ChromeDriverManager(path='temp/driver_path').install(), options=options)
        return driver

    else:
        options.add_argument(argument=f'user-agent={random.choice(user_agent)}')
        options.add_argument(argument='--incognito')
        driver = webdriver.Chrome(ChromeDriverManager(path='temp/driver_path').install(), options=options)
        return driver
