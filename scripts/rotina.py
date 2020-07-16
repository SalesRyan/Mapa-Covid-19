import schedule
import time
from scripts.atualizar import verification
from dashboard.models import DataAtualizacao

def job():
    verification()

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)