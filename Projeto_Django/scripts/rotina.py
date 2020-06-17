import schedule
import time
from scripts.atualizar import verification

def job():
    verification()

schedule.every(30).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)