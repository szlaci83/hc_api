import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from properties import *
from mail_repo import create_invite_mail, create_reg_mail


def _sendmail(to, subject, html, text):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = FROM_ADDR
    msg['To'] = to

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP(SMTP)
    server.ehlo()
    server.starttls()
    server.login(FROM_ADDR, PW)
    server.sendmail(FROM_ADDR, to, msg.as_string())
    server.quit()


def send_reg_mail(to_mail, name, link):
    html, text = create_reg_mail(name, link)
    _sendmail(to_mail, REG_SUBJECT, html, text)


def send_invite_mail(to_mail, from_user_name, invited_user_name):
    html, text = create_invite_mail(from_user_name, invited_user_name)
    _sendmail(to_mail, INVITE_SUBJECT, html, text)


def _example():
    send_reg_mail(TEST_EMAIL, "Lacc1", "1dsf86df2774")
    send_invite_mail(TEST_EMAIL, "user11", "user2")


if __name__ == "__main__":
    _example()

