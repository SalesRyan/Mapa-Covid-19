import schedule
import time
from scripts.atualizar import verification
from dashboard.models import DataAtualizacao

def job():
    verification()

#schedule.every(2).hours.do(job)
schedule.every().day.at("16:00").do(job)
schedule.every().day.at("19:00").do(job)
schedule.every().day.at("20:00").do(job)
schedule.every().day.at("02:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)