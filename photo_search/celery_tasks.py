from typing import List
from photo_search_iitsyndicate.celery import app as celery_app
from .utils import send_emails, parse_emails_file


@celery_app.task
def send_emails_from_file(filename: str, text: str) -> None:
    emails = parse_emails_file(filename)
    send_emails(emails, text)
