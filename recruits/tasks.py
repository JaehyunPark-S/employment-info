from static.python import stackoverflow_crawler as sc

from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def so_crawler():
    last_page = sc.get_last_page()
    sc.extract_jobs(3)
