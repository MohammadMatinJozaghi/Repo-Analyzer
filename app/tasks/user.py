from app.core.celery import celery_app
from app.utils.send_email import send_email


@celery_app.task
def send_email_task(email:str,code:int): 
    send_email(
        email, 
        'ادامه ی ثبت نام', 
        f'کد تایید جهت تکمیل ثبت نام : {code}'
    )