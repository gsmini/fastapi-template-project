import smtplib
from email.mime.text import MIMEText
from src import config


def send(subject, content, send_to):
    """

    :param subject: 邮件主题
    :param content: 邮件内容

    :param send_to: 接收者
    :return:
    """
    try:
        msg = MIMEText(content, 'html', 'utf-8')  # html表示内容可以为html 否则无法渲染内容
        msg['From'] = config.EMAIL_FROM_SEND  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = send_to  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = subject  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL(config.EMAIL_SMTP_SERVER, config.EMAIL_SMTP_PORT)  # 发件人邮箱中的SMTP服务器
        server.login(config.EMAIL_FROM_SEND, config.EMAIL_SENDER_AUTH_CODE)  # 括号中对应的是发件人邮箱账号、邮箱授权码
        server.sendmail(config.EMAIL_FROM_SEND, send_to, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print("xx", e)
    return


# redis的缓存key
def get_email_code_key(email, email_type, code):
    return f"{email}_{email_type}:{code}"


# 注册模版
def get_register_email_content(email, code):
    """

    :param email: 接受者邮箱
    :param code: 验证码
    :return: 邮件内容 和邮件主题
    """
    return f"""
        <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>Reset the password verification code</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Microsoft Yahei', sans-serif; background-color: #fff;">
        <!-- 用表格实现布局，确保各客户端兼容 -->
        <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
                <td style="padding: 0;">
                    <!-- 蓝色分割线 -->
                    <div style="height: 3px; background-color: #4285f4; margin-bottom: 40px;"></div>
                </td>
            </tr>
            <tr>
                <td style="text-align: center; padding-bottom: 20px;">
                    <p style="font-size: 18px; color: #333; margin: 0;">Registration verification code</p>
                </td>
            </tr>
            <tr>
                <td style="text-align: center; padding-bottom: 30px;">
                    <p style="font-size: 36px; color: #4285f4; font-weight: bold; margin: 0;">{code}</p>
                </td>
            </tr>
            <tr>
                <td style="text-align: center; padding-bottom: 10px;">
                    <p style="font-size: 14px; color: #666; margin: 0;">Used to verify registration verification code：</p>
                </td>
            </tr>
            <tr>
                <td style="text-align: center; padding-bottom: 50px;">
                    <a style="font-size: 14px; color: #4285f4; text-decoration: none; margin: 0;">{email}</a>
                </td>
            </tr>
            <tr>
                <td style="text-align: center; padding-bottom: 20px;">
                    <p style="font-size: 12px; color: #999; margin: 0;">This verification code is valid for 30 minutes. Please proceed to the next step immediately</p>
                </td>
            </tr>
        </table>
    </body>
    </html>
""", "register your account"


# 忘记密码模版
def get_forget_pwd_email_content(email, code):
    """

        :param email: 接受者邮箱
        :param code: 验证码
        :return: 邮件内容 和邮件主题
    """
    return f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Reset the password verification code</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Microsoft Yahei', sans-serif; background-color: #fff;">
    <!-- 用表格实现布局，确保各客户端兼容 -->
    <table width="100%" border="0" cellspacing="0" cellpadding="0">
        <tr>
            <td style="padding: 0;">
                <!-- 蓝色分割线 -->
                <div style="height: 3px; background-color: #4285f4; margin-bottom: 40px;"></div>
            </td>
        </tr>
        <tr>
            <td style="text-align: center; padding-bottom: 20px;">
                <p style="font-size: 18px; color: #333; margin: 0;">Reset the password verification code</p>
            </td>
        </tr>
        <tr>
            <td style="text-align: center; padding-bottom: 30px;">
                <p style="font-size: 36px; color: #4285f4; font-weight: bold; margin: 0;">{code}</p>
            </td>
        </tr>
        <tr>
            <td style="text-align: center; padding-bottom: 10px;">
                <p style="font-size: 14px; color: #666; margin: 0;">Used to verify your account：</p>
            </td>
        </tr>
        <tr>
            <td style="text-align: center; padding-bottom: 50px;">
                <a style="font-size: 14px; color: #4285f4; text-decoration: none; margin: 0;">{email}</a>
            </td>
        </tr>
        <tr>
            <td style="text-align: center; padding-bottom: 20px;">
                <p style="font-size: 12px; color: #999; margin: 0;">This verification code is valid for 30 minutes. Please proceed to the next step immediately</p>
            </td>
        </tr>
    </table>
</body>
</html>
""", "reset your password"


if __name__ == "__main__":
    # SMTP服务器信息

    subject = "测试报告"
    send_to = "gsmini@sina.cn"
    send(subject, get_register_email_content(send_to, "12234558"), send_to)
