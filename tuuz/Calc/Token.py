import hashlib
import random
import time
from datetime import datetime

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
    return "D" + datetime.now().strftime("%Y%m%dT%H%M%S") + "U" + string + "R" + str(base_num)


def refresh_base_num():
    print("订单indexpts刷新启用")
    global base_num
    while True:
        base_num = 0
        print("indexpts")
        time.sleep(1)


def md5(string):
    return hashlib.md5(string.encode()).hexdigest()
