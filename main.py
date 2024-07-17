from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import telegram
import asyncio
import logging

logging.basicConfig(filename='hp-boot.log', level=logging.INFO)
LOGIN = os.environ.get("LOGIN")
PASSWORD = os.environ.get("PASSWORD")
IP_PRINTS = os.environ.get("IP_PRINTS").split(",")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)

def reinicia(ip_print):
    driver.get(f"https://{LOGIN}:{PASSWORD}@{ip_print}/#hId-pgPowerCycle")
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="button"]'))
    ).click()
    driver.find_element(By.CLASS_NAME, "gui-cmd-bar-btn-power_cycle").click()
    driver.implicitly_wait(3)
    driver.find_element(
        By.XPATH, "//button[@class='gui-action-btn' and text()='Sim']"
    ).click()
    driver.implicitly_wait(3)

def nivel_tooner(ip_print):
    driver.get(f"https://{ip_print}/#hId-pgConsumables")
    saida=[]
    xpath_nivel = "/html/body/div[1]/div[5]/div[1]/div[2]/form/div[1]/div[2]/div[1]/div/table/tbody/tr[8]/td[2]"
    xpath_ult = "/html/body/div[1]/div[5]/div[1]/div[2]/form/div[1]/div[2]/div[1]/div/table/tbody/tr[4]/td[2]"
    xpath_instalacao = "/html/body/div[1]/div[5]/div[1]/div[2]/form/div[1]/div[2]/div[1]/div/table/tbody/tr[5]/td[2]"
    saida.append(ip_print)
    #for xpath in [xpath_nivel, xpath_ult, xpath_instalacao]:
    try:
        saida.append(WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_nivel))).text)
        if saida[1] == "> 8000 †":
                saida[1] = "8000"
        saida.append(WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_ult))).text)
        saida.append(WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_instalacao))).text)
    except Exception as e:
        logging.error({str(e)})
    
    saida = f"\n{saida[0]}\t{saida[1]}\t\t{saida[2]}\t{saida[3]}"
    return saida
    #return [ip_print, pg_restantes.text, ultima_boot.text, toner_instalacao.text]

async def envia_mensagem(mensagem):
    try:
        bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
        async with bot:
            await bot.send_message(text=mensagem, chat_id=TELEGRAM_CHAT_ID)
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem: {str(e)}")
        return False
    return True

if __name__ == "__main__":
    logging.info("-----Iniciando-----")
    saida = f"Ip Impr.\tEstimativa\tÚlt.util\tInst.Toner"
    for ip_print in IP_PRINTS:
        cont_erro = 0
        try:
            nivel = nivel_tooner(ip_print)
            saida += nivel
            logging.info(nivel)
            #reinicia(ip_print)
        except Exception as e:
            if cont_erro < 1:
                time.sleep(1)
                nivel = nivel_tooner(ip_print)
                saida += nivel
                logging.info(nivel)

            cont_erro += 1
            logging.error(f"Erro ao acessar {ip_print}: {str(e)}")

    driver.quit()
    asyncio.run(envia_mensagem(saida))
    print(saida)
    
