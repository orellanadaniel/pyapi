
from selenium.webdriver.common.keys import Keys
# Selenium Explicit Waits
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxProfile, Chrome
from time import strftime,sleep
import datetime, os

url = 'http://certificados.ministeriodegobierno.gob.ec/gestorcertificados/antecedentes/'

class selenium:
    wait = True
    
    def __init__(self):
        self.driver = self.iniciar()
        print('Iniciado Webdriver')
        pass

    def iniciar(self): # Inicializar Webdriver
        try:
            gc = Options()
            gc.add_argument('user-data-dir=sel')
            if os.name == 'nt':
                print('Operative System> Windows')
                return Chrome(options=gc, executable_path='./app/drivers/chromedriver.exe')
            else:
                print('Operative System> Unix')
                gc.add_argument('headless')
                gc.add_argument('no-sandbox')
                return Chrome(options=gc, executable_path='./app/drivers/chromedriver')
        except Exception as e:
            print(e)
        finally:
            pass

    def button_click(self, button, timeout): # Buscar boton
        #print(button)
        try:
            #btn = driver.find_element_by_xpath(button)
            btn = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, button))) # presence_of_element_located
            btn.click()
            return True
        except:
            return False

    def pass_text(self, text, tagid, timeout): # Pasar texto a elementos
        #print(tagid)
        try:
            #motivo = self.driver.find_element_by_xpath('//*[@id="{}"]'.format(tagid))
            motivo = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, tagid))) # presence_of_element_located
            motivo.send_keys(text)
            return True
        except:
            return False

    def run(self, ci): # Main
        re = {}
        try:
            self.wait = False
            self.driver.get(url)
            startscript = datetime.datetime.now()
            #print(self.driver.title)
            self.button_click('/html/body/div[5]/div[11]/button[2]/span', 5) # Warning button
            self.pass_text(ci, 'txtCi', 5)
            self.button_click('//*[@id="btnSig1"]', 5) # Search button
            if self.pass_text('Consulta antecedentes', 'txtMotivo', 15):
                self.button_click('//*[@id="btnSig2"]', 5) # Motivo button
                #self.driver.implicitly_wait(2) # seconds
                name = self.driver.find_element_by_id('dvName1')
                antecedentes = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "dvAntecedent1"))) # presence_of_element_located
                endscript = datetime.datetime.now()
                duration = endscript - startscript
                re = {'CI': ci,'Name': str(name.text), 'Antecedentes': str(antecedentes.text), 'response': '{}'.format(str(duration))}
            else:
                re = {'error': 'ci not found'}
        except Exception as e:
            print(e)
            return {'error': 'error'}
        finally:
            self.wait = True
            return re