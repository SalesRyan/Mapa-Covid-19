import schedule
import time
from scripts.agrupamentos.povoar_atualizar_financeiro import verificar

schedule.every().day.at("00:01").do(verificar)

while True:
    schedule.run_pending()
    time.sleep(1)