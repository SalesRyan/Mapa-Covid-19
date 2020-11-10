import schedule
import time
from scripts.agrupamentos.povoar_atualizar_financeiro import verificar

# schedule.every().day.at("0:00").do(verificar)
schedule.every().day.at("0:01").do(verificar)

while True:
    schedule.run_pending()
    time.sleep(1)