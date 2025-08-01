from typing import Union

from django.conf import settings
from django.core.mail import send_mail


def send_email(subject, message, to_email:Union[str, list[str]]) :
    to_email = to_email if isinstance(to_email, list) else [to_email]
    # 리스트 형태로 만들어 줌

    send_mail(subject, message, settings.EMAIL_HOST_USER, to_email)
