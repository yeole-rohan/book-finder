# tasks.py

from celery import shared_task

@shared_task
def my_task():
    # Your task logic here
    result = 10 + 10
    return result
