from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import telegram
import asyncio

LOGIN = os.environ.get('LOGIN')
PASSWORD = os.environ.get('PASSWORD')
IP_PRINTS = os.environ.get('IP_PRINTS').split(",")
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
niveis_tooner=[]
saida="Nível de tooner das impressoras:\n"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def reinicia(ip_print):
    driver.get(f"https://{LOGIN}:{PASSWORD}@{ip_print}/#hId-pgPowerCycle")
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//input[@type="button"]'))).click()
    driver.find_element(By.CLASS_NAME, "gui-cmd-bar-btn-power_cycle").click()
    driver.implicitly_wait(3)
    driver.find_element(By.XPATH, "//button[@class='gui-action-btn' and text()='Sim']").click()
    driver.implicitly_wait(3)

def nivel_tooner(ip_print):
    driver.get(f"https://{ip_print}/#hId-pgConsumables")
    xpath_nivel="/html/body/div[1]/div[5]/div[1]/div[2]/form/div[1]/div[2]/div[1]/div/table/tbody/tr[8]/td[2]"
    xpath_boot="/html/body/div[1]/div[5]/div[1]/div[2]/form/div[1]/div[2]/div[1]/div/table/tbody/tr[4]/td[2]"
    pg_restantes=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_nivel)))
    ultima_boot=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_boot)))
    return [ip_print,pg_restantes.text,ultima_boot.text]

async def envia_mensagem(mensagem):
    try:
        bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
        async with bot:
            await bot.send_message(text=mensagem, chat_id=TELEGRAM_CHAT_ID)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {str(e)}")
        return False
    return True

for ip_print in IP_PRINTS:
    try:
        nivel=nivel_tooner(ip_print)
        print(nivel)
        #if int(nivel[1])<500:
        niveis_tooner.append(nivel)
        saida+=f"{nivel[0]} {nivel[1]} {nivel[2]}\n"
        #reinicia(ip_print)
    except Exception as e:
        print(f"Erro ao acessar {ip_print}: {str(e)}")

driver.quit()

print(saida)
#if saida != "Nível de tooner das impressoras:\n":
asyncio.run(envia_mensagem(saida))
