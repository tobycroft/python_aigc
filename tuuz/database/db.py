import configparser

import config


async def init():
    cfg = configparser.ConfigParser()
    cfg.read("conf.ini")
    if "database" not in cfg:
        cfg["database"] = {
            "need": "true",
            "retry": "false",
            "dbname": "",
            "dbuser": "",
            "dbpass": "",
            "dbhost": "",
            "dbport": ""
        }
        with open("conf.ini", "w") as configfile:
            cfg.write(configfile)
        print("database_ready")
        await init()
    else:
        section = cfg["database"]
        config.db.need = section.get("need", "")
        config.db.retry = section.get("retry", "")
        config.db.dbname = section.get("dbname", "")
        config.db.dbuser = section.get("dbuser", "")
        config.db.dbpass = section.get("dbpass", "")
        config.db.dbhost = section.get("dbhost", "")
        config.db.dbport = section.get("dbport", "")
    print("database:ready")
