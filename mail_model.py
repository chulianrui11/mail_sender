import smtplib
from email.header import Header
from email.mime.text import MIMEText


class Mail(object):

    def __init__(self, host, sender=None, password=None, title=None):
        self.host = host
        self.sender = sender
        self.password = password
        self.title = title

    def _init_server(self):
        server = smtplib.SMTP(self.host)
        if self.sender and self.password:
            server.login(self.sender, self.password)
        return server

    def _validate_users(self, users):
        if not isinstance(users, list):
            users = users.split(',')
        user_list = []
        for user in users:
            _user = user.split('@')
            if len(_user) != 2 or (len(_user) == 2 and not _user[1]):
                user_list.append(f'{_user[0]}@17zuoye.com')
            else:
                user_list.append(user)
        return ','.join(user_list)

    def send(self, subject, sendto, message, **kwargs):
        sendto = self._validate_users(sendto)
        kwargs['_subtype'] = 'plain'
        server = self._init_server()
        msg = MIMEText(message, **kwargs)
        msg['From'] = self.sender
        msg['To'] = sendto
        msg['Subject'] = Header(subject)

        server.sendmail(self.sender, sendto.split(','), msg.as_string())
        server.close()

    def send_html(self, subject, sendto, message, **kwargs):
        kwargs['_subtype'] = 'html'
        self.send(subject, sendto, message, **kwargs)
