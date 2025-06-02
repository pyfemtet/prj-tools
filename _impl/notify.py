import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from load_secret import secret
except ModuleNotFoundError:
    from .load_secret import secret


__all__ = ['send_mail']


# GmailのSMTPサーバー情報
smtp_server = secret['SMTP_SERVER']
smtp_port = secret['SMTP_PORT']

# 送信者のメールアドレスとパスワード
sender_email = secret['NOTIFICATION_FROM']

def send_mail(subject: str, body: str, html_file_path: str = None):

    body = body.replace('\\n', '\n')

    print()
    print('<subject>')
    try:
        print(subject)
    except UnicodeEncodeError:
        # print(subject.encode('cp932', 'ignore').decode('cp932'))
        print(
            body.replace(
                '✅', '[P]'
            ).replace(
                '🔥', '[F]'
            ).replace(
                '💤', '[S]'
            ).replace(
                '❔', '[?]'
            )
        )
    print()
    print('<body>')
    try:
        print(body)
    except UnicodeEncodeError:
        # print(body.encode('cp932', 'ignore').decode('cp932'))
        print(
            body.replace(
                '✅', '[P]'
            ).replace(
                '🔥', '[F]'
            ).replace(
                '💤', '[S]'
            ).replace(
                '❔', '[?]'
            )
        )
    print()

    # 受信者のメールアドレス
    receiver_email = ';'.join(secret['NOTIFICATION_TO'])

    if not receiver_email:
        return

    # メールの作成
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # report html の添付
    if html_file_path is not None:
        if os.path.isfile(html_file_path):
            with open(html_file_path, 'rb') as f:
                mime_base = MIMEBase('text', 'html')
                mime_base.set_payload(f.read())
                encoders.encode_base64(mime_base)
                mime_base.add_header('Content-Disposition', f'attachment; filename="{html_file_path.split("/")[-1]}"')
                msg.attach(mime_base)
        else:
            body = '添付すべき html ファイルが見つかりませんでした。\n\n' + body

    # 本文をメールに添付
    msg.attach(MIMEText(body, 'plain'))

    # SMTPサーバーに接続（暗号化なし）
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # ログインが不要な場合はloginしなくてOK
        server.sendmail(sender_email, receiver_email, msg.as_string())


if __name__ == '__main__':
    send_mail(sys.argv[1], sys.argv[2])
