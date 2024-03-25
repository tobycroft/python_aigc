import hashlib
import random
import time
from datetime import datetime
from threading import Timer

base_num = 0


def generate_token():
    unix = int(time.time() * 1000000000)
    rand = random.randint(0, 99999999)
    string = str(unix) + str(rand)
    return md5(string)


def generate_order_id():
    global base_num
    base_num += 1
    string = str(int(time.time())) + str(base_num)
    return datetime.now().strftime("%-D%Y%m%dT%H%M%SU") + string + "R" + str(base_num)


def refresh_base_num():
    global base_num
    base_num = 0
    Timer(1, refresh_base_num).start()


def md5(string):
    return hashlib.md5(string.encode()).hexdigest()


# Start refreshing the base number
refresh_base_num()
