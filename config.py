APP_VERSION = '4.9.1'
API_VERSION = 'v2.5'
ANDROID_OS = 'android 5.0'
COUNTRY = 'RU'
HMAC_KEY = "2Wq7)qkX~cp7)H|n_tc&o+:G_USN3/-uIi~>M+c ;Oq]E{t9)RC_5|lhAA_Qq%_4"


class Config1:
    TOKEN = 'TOKEN'
    AES_KEY = 'AES_KEY'
    PRIVATE_KEY = int('PRIVATE_KEY')
    DEVICE_ID = 'DEVICE_ID'


class Config2:
    TOKEN = 'TOKEN'
    AES_KEY = 'AES_KEY'
    PRIVATE_KEY = int('PRIVATE_KEY')
    DEVICE_ID = 'DEVICE_ID'


configs = [globals()[cl]() for cl in globals() if 'Config' in cl]
