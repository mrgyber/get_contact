from threading import Lock
import json
import time

import requests

from config import APP_VERSION, API_VERSION, ANDROID_OS, COUNTRY
from getcontact.decode_captcha import CaptchaDecode
from getcontact.cipher import Cipher

captcha_lock = Lock()


class Requester:
    def __init__(self, config, verbose, lock_logger):
        self.config = config
        self.verbose = verbose
        self.lock_logger = lock_logger

        self.base_url = ''
        self.base_uri_api = ''
        self.methods = {}
        self.headers = {}
        self.request_data = {}

        self.current_task = {}

        self.timestamp = ''

        self.cipher = Cipher(config)
        self.update_timestamp()
        self.set_dict()

    def set_dict(self):
        self.base_url = "https://pbssrv-centralevents.com"
        self.base_uri_api = f"/{API_VERSION}/"
        self.methods = {"number-detail": "details",
                        "verify-code": ""}

        self.headers = {"X-App-Version": APP_VERSION,
                        "X-Token": self.config.TOKEN,
                        "X-Os": ANDROID_OS,
                        "X-Client-Device-Id": self.config.DEVICE_ID,
                        "Content-Type": "application/json; charset=utf-8",
                        "Connection": "close",
                        "Accept-Encoding": "gzip, deflate",
                        "X-Req-Timestamp": self.timestamp,
                        "X-Req-Signature": "",
                        "X-Encrypted": "1"}

        self.request_data = {"countryCode": COUNTRY,
                             "source": "",
                             "token": self.config.TOKEN}

    def update_config(self):
        self.cipher.update_config()
        self.set_dict()

    def update_timestamp(self):
        self.timestamp = str(time.time()).split('.')[0]

    def _parse_response(self, response):
        if response.status_code == 200:
            return True, response.json()["data"]
        if response.status_code == 201:
            return True, response.json()
        else:
            response = response.json()['data']
            response = json.loads(self.cipher.decrypt_aes_b64(response))
            error_code = response['meta']['errorCode']

            if error_code == '403004':
                if self.verbose > 1:
                    self.lock_logger.acquire()
                    print(f"\033[38;2;255;255;0m[CAPTCHA]\033[38;2;255;255;255m")
                    self.lock_logger.release()

                captcha_lock.acquire()
                c = CaptchaDecode()
                code, path = c.decode_response(response)
                captcha_lock.release()

                self.update_config()
                captcha_data = {"token": self.config.TOKEN,
                                "validationCode": code}
                self.send_req_to_the_server(self.base_url + self.base_uri_api + 'verify-code', captcha_data)

                return False, {'repeat': True}
            if error_code == '404001':
                print('No information about phone in database')

            return False, {}

    def send_req_to_the_server(self, url, payload):
        payload = json.dumps(payload).replace(" ", "").replace("~", " ")
        self.headers["X-Req-Signature"] = self.cipher.create_signature(payload, self.timestamp)
        self.headers["X-Encrypted"] = "1"
        response = requests.post(url, data=json.dumps({"data": self.cipher.encrypt_aes_b64(payload)}),
                                 headers=self.headers)
        self.update_timestamp()
        is_ok, response = self._parse_response(response)

        if is_ok:
            return json.loads(self.cipher.decrypt_aes_b64(response))
        elif not is_ok and 'repeat' in response.keys() and response['repeat']:
            phone = self.current_task['phone']
            return self.get_phone_tags(phone)
        else:
            return response

    def get_phone_tags(self, phone_number):
        self.current_task = {'function': 'get_phone_tags', 'phone': phone_number}

        self.update_config()
        method = "number-detail"
        self.request_data["source"] = self.methods[method]
        self.request_data["phoneNumber"] = phone_number
        return self.send_req_to_the_server(self.base_url + self.base_uri_api + method, self.request_data)
