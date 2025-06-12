import smtplib
from email.mime.text import MIMEText
from abc import ABC, abstractmethod
from enum import StrEnum
from repository import repo

class Role(StrEnum):
    DIRECTOR = 'parfeniukink@gmail.com'
    ADMINISTRATION = 'administratiom@gmail.com'

class Subject(StrEnum):
    DAILY_REPORT = 'Daily Report'
    MONTHLY_REPORT = 'Monthly Report'


class Message:
    def __init__(self, from_addr: str, to: str, subject: str, message: str):
        self.msg = MIMEText(message)
        self.msg['To'] = to
        self.msg['Subject'] = subject
        self.msg['From'] = from_addr


    @property
    def sender(self) -> str:
        return self.msg['From']

    @property
    def recipient(self) -> str:
        return self.msg['To']


class SMTPService:
    def __init__(self, host: str = "localhost", port: int = 1025):
        self.host = host
        self.port = port

    def __enter__(self):
        self.server = smtplib.SMTP(host=self.host, port=self.port)
        return self

    def __exit__(self, *args, **kwargs):
        self.server.quit()

    def send(self, from_: str, to: str, message: Message) -> None:
        self.server.sendmail(msg=message.msg.as_string(), from_addr=from_, to_addrs=to)


class SendEmail(ABC):
    def __init__(self, from_addr: str, to: str, subject: str, message_text: str):
        self.from_addr = from_addr
        self.to = to
        self.subject = subject
        self.message_text = message_text
        self.message = Message(self.from_addr, self.to, self.subject, self.message_text)

    @abstractmethod
    def send_report(self):
        with SMTPService() as mailing:
            mailing.send(from_=self.message.sender, to=self.message.recipient, message=self.message)


class SendEmailWithDailyReport(SendEmail):

    def __init__(self):
        marks_list = repo.get_all_marks_today()

        if marks_list:
            avg_mark = sum(marks_list) / len(marks_list)
        else:
            avg_mark = 0

        text = (f"Hello, new daily report available.\n"
                            f"Average students mark today: {avg_mark}\n\n"
                            f"Administration Department")
        super().__init__(Role.ADMINISTRATION, Role.DIRECTOR, Subject.DAILY_REPORT, text)


    def send_report(self):
        with SMTPService() as mailing:
            mailing.send(from_=self.message.sender, to=self.message.recipient, message=self.message)


class SendEmailWithMonthlyReport(SendEmail):

    def __init__(self):
        marks_list = repo.get_all_marks_per_month()

        if marks_list:
            avg_mark = sum(marks_list) / len(marks_list)
        else:
            avg_mark = 0

        text = (f"Hello, new monthly report available.\n"
                            f"Average students mark for the last month: {avg_mark}\n\n"
                            f"Administration Department")
        super().__init__(Role.ADMINISTRATION, Role.DIRECTOR, Subject.MONTHLY_REPORT, text)


    def send_report(self):
        with SMTPService() as mailing:
            mailing.send(from_=self.message.sender, to=self.message.recipient, message=self.message)






