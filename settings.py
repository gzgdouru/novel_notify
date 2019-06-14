# 邮件配置
EMAIL_HOST = "smtp.163.com"
EMAIL_USER = "gzouru@163.com"
EMAIL_PASSWORD = "qq5201314ouru"

# 数据库配置
DB_NAME = "novel"
DB_USER = "ouru"
DB_PASSWORD = "5201314Ouru..."
DB_HOST = "47.101.192.184"
DB_PORT = 3306
DB_CHARSET = "utf8"

# 小说配置
NOVELS = [
    {
        "name": "全职法师",
        "url": "https://www.dingdiann.com/ddk23863",
        "receivers": ["18719091650@163.com", "mabodxbs@gmail.com"],
        "parser": "dingdian",
    }
]

# 基础配置
CONCURRENCY = 5
