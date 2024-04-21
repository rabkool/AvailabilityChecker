import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# 商品url
# url = "https://www.amazon.co.jp/dp/B07GST7328"

# 测试url
url = "https://www.amazon.co.jp/dp/B0BCF3VRJV"

# 设置邮件参数
email_sender = "你的邮箱@gmail.com"
email_receiver = "收件人的邮箱@gmail.com"
email_subject = "有货提醒"
email_body = f"商品 {url} 有货!"

# 邮箱登录信息
# 注意：要打开邮箱2段階認証 https://myaccount.google.com/security?hl=ja
email_username = "你的邮箱@gmail.com"

# 生成应用密码的步骤：https://myaccount.google.com/apppasswords?pli=1&rapt=AEjHL4OLT9SmujePkRJd1lB-NBFaNRaFG2THMBlic3KVlu8_aTykSVVtURSJbm6j9pf57-9EGnlC7y0dqP_PqRLVS3hTPIR5Ew
# 在 "アプリを選択" 中选择 "その他（名前を入力）"，输入任意名称，然后点击 "生成" 按钮即可获得16位的应用密码。
email_password = "16位的应用密码"

# 发送邮件
def send_email():
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_username, email_password)
    text = msg.as_string()
    server.sendmail(email_sender, email_receiver, text)
    server.quit()

# 检查商品是否有货
def check_availability():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    offer_section = soup.find("span", {"data-action": "show-all-offers-display"})
    
    if offer_section:
        availability_msg = offer_section.find("span", {"class": "a-size-medium a-color-success"})
        if availability_msg and "現在在庫切れです" in availability_msg.text:
            print("无货")
        else:
            send_email()

# 主循环
try:
    while True:
        check_availability()
        # 设置检查商品时间 60（60秒）
        time.sleep(60)
except KeyboardInterrupt:
    print("手动停止")