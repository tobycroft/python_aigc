import configparser
import os

# 定义一些默认值
Project = "tuuzgoweb"
Debug = "tgw"
TestMode = True
AppMode = "debug"
WebsocketKey = ""


async def init():
    global Project, Debug, TestMode, AppMode, WebsocketKey
    if not os.path.exists("conf.ini"):
        cfg = configparser.ConfigParser()
        cfg.add_section("app")
        cfg.set("app", "Project", Project)
        cfg.set("app", "Debug", Debug)
        cfg.set("app", "TestMode", str(TestMode))
        cfg.set("app", "AppMode", AppMode)
        cfg.set("app", "WebsocketKey", WebsocketKey)
        with open("conf.ini", "w") as configfile:
            cfg.write(configfile)
        print("app_ready")
        await init()
    else:
        cfg = configparser.ConfigParser()
        cfg.read("conf.ini")
        if not cfg.has_section("app"):
            cfg.add_section("app")
            cfg.set("app", "Project", Project)
            cfg.set("app", "Debug", Debug)
            cfg.set("app", "TestMode", str(TestMode))
            cfg.set("app", "AppMode", AppMode)
            cfg.set("app", "WebsocketKey", WebsocketKey)
            with open("conf.ini", "w") as configfile:
                cfg.write(configfile)
            print("app_ready")
            await init()
        else:
            Project = cfg.get("app", "Project")
            Debug = cfg.get("app", "Debug")
            TestMode = cfg.getboolean("app", "TestMode")
            AppMode = cfg.get("app", "AppMode")
            WebsocketKey = cfg.get("app", "WebsocketKey")
    print("系统环境加载完毕")
    if TestMode:
        print("系统正处于测试模式，测试密钥：", Debug)
