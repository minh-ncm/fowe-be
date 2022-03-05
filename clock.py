import os
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger


scheduler = BlockingScheduler()
trigger_vn = OrTrigger([
    CronTrigger(day_of_week='mon-fri', hour='9-10', minute='*/15', timezone='Asia/Ho_Chi_Minh'),
    CronTrigger(day_of_week='mon-fri', hour='13-14', minute='*/15', timezone='Asia/Ho_Chi_Minh'),
    CronTrigger(day_of_week='mon-fri', hour='11', minute='0,15,30', timezone='Asia/Ho_Chi_Minh'),
    CronTrigger(day_of_week='mon-fri', hour='15', minute='0', timezone='Asia/Ho_Chi_Minh'),
])


@scheduler.scheduled_job(trigger_vn)
def fetch_stock_vn():
    os.system('python manage.py fetch-stock-vn')


trigger_clean_postgress = CronTrigger(day_of_week='mon-fri', hour='15', minute='30', timezone='Asia/Ho_Chi_Minh')
@scheduler.scheduled_job(trigger_clean_postgress)
def clean_postgress():
    os.system('python manage.py upload-stock-vn')


trigger_us = CronTrigger(day='1', hour='0', minute='0', timezone='US/Eastern')
@scheduler.scheduled_job(trigger_us)
def fetch_stock_us():
    os.system(('python manage.py fetch-stock-us'))


trigger_flush_jwt = CronTrigger(hour="12", minute='0', timezone='Asia/Ho_Chi_Minh')
@scheduler.scheduled_job(trigger_flush_jwt)
def flush_jwt():
    os.system('python manage.py flushexpiredtokens')


scheduler.start()
