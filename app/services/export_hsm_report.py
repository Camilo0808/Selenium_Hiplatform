import os
import sys

# Add your project directory to your sys.path
project_home = os.environ.get("PROJECT_HOME", "/app")
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from app.database.connection import Database

from datetime import datetime, timedelta
import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from settings import FILE_PATH, PASSWORD, TABLE_NAME, URL, LOGIN
from time import sleep


class MyException(Exception):
    pass

class ExportHSM:
    def __init__(self) -> None:
        self.file_path = FILE_PATH
        self.password = PASSWORD
        self.table_name = TABLE_NAME
        self.username = LOGIN
        self.url = URL

    # Searches for the downloaded file by its partial name
    def search_file(self) -> list:
        all_files = os.listdir(self.file_path)
        file_found = [file for file in all_files if "WhatsAppHSM_" in file and file.endswith(".csv")]
        return file_found

    def export_report(self) -> bool:
        # Initializing automated navigator
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('enable-automation')
        options.add_argument('--disable-infobars')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')
        nav = webdriver.Chrome(options=options)
        nav.get(self.url)

        # Website Login stage 
        login_path = "login"
        pwd_path = "password"
        login_button_path = "loginButton"

        WebDriverWait(nav, 25).until(
            EC.presence_of_element_located((By.ID, login_path))
        )
        nav.find_element(By.ID, login_path).send_keys(self.username)
        nav.find_element(By.ID, pwd_path).send_keys(self.password)
        nav.find_element(By.ID, login_button_path).click()

        # Navigates to the reports tab and wait for the page to load
        relatorios_tab_path = '//*[@id="nav--mega"]/div/div/ul/li[2]/p'
        WebDriverWait(nav, 25).until(
            EC.presence_of_element_located((By.XPATH, relatorios_tab_path))
        )
        nav.find_element(By.XPATH, relatorios_tab_path).click()

        # Navigates to the reports extraction tab and wait for the page to load
        exportacoes_path = '//*[@id="#"]/ul/li[1]/span/ul/li[10]/a'
        WebDriverWait(nav, 25).until(
            EC.presence_of_element_located((By.XPATH, exportacoes_path))
        )
        element = nav.find_element(By.XPATH, exportacoes_path)
        nav.execute_script("arguments[0].click();", element)

        # Apllying date filters and downloading CSV file
        yesterday = datetime.now().date() - timedelta(days=1)

        if int(yesterday.day) < 10:
            filter_date = f"0{yesterday.day}0{yesterday.month}{yesterday.year}"
        else:
            filter_date = f"{yesterday.day}0{yesterday.month}{yesterday.year}"

        # Waits for the page to load
        nav.implicitly_wait(8)

        apply_button = '//*[@id="filter-menu"]/div[3]/ul/div[2]/button'
        iframes = nav.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            nav.switch_to.frame(iframe)
            try:
                nav.find_element(By.CLASS_NAME, "css-i9m92").click()
                nav.implicitly_wait(2)
                elements = nav.find_elements(By.XPATH, '//*[@id="filter-menu"]/div[3]/ul')
                for element in elements:
                    date_from = element.find_element(By.ID, "mui-8")
                    date_from.click()
                    date_from.send_keys(Keys.BACKSPACE)
                    date_from.send_keys(Keys.BACKSPACE)
                    date_from.send_keys(Keys.BACKSPACE)
                    date_from.send_keys(Keys.BACKSPACE)
                    date_from.send_keys(Keys.BACKSPACE)
                    date_from.send_keys(Keys.BACKSPACE)
                    date_from.send_keys(Keys.BACKSPACE)
                    date_from.send_keys(Keys.BACKSPACE)
                    date_from.send_keys(filter_date)
                    continue
                for element in elements:
                    date_to = element.find_element(By.ID, "mui-10")
                    date_to.click()
                    date_to.send_keys(Keys.BACKSPACE)
                    date_to.send_keys(Keys.BACKSPACE)
                    date_to.send_keys(Keys.BACKSPACE)
                    date_to.send_keys(Keys.BACKSPACE)
                    date_to.send_keys(Keys.BACKSPACE)
                    date_to.send_keys(Keys.BACKSPACE)
                    date_to.send_keys(Keys.BACKSPACE)
                    date_to.send_keys(Keys.BACKSPACE)
                    date_to.send_keys(filter_date)
                    date_to.click()
                    continue
                button = nav.find_element(By.XPATH, apply_button)
                button.click()
                botao_exportar_path = '//*[@id="root"]/div/div/main/div[4]/div[1]/button'
                WebDriverWait(nav, 15).until(
                    EC.element_to_be_clickable((By.XPATH, botao_exportar_path))
                )
                nav.find_element(By.XPATH, botao_exportar_path).click()
                break
            except: 
                pass

        # Waits for the file to be downloaded
        files = self.search_file()
        attempts = 0

        while len(files) == 0:
            if attempts > 3:
                raise MyException("Exceeded attempts")
            sleep(6)
            files = self.search_file()
            attempts += 1

        # Reads the CSV file, creates a pandas DataFrame and updates the table database table
        try:
            engine = Database().database_connection()
            csv = pd.read_csv(self.file_path + files[0], sep=";", encoding="utf-16le", usecols=np.arange(14))
            
            df_csv = pd.DataFrame(csv)
            df_csv['remetente'] = df_csv['remetente'].astype(str)
            df_csv['destinatário'] = df_csv['destinatário'].astype(str)
            df_csv.to_sql(self.table_name, con=engine, if_exists='append', index=False)
            print(df_csv)
            os.remove(self.file_path + files[0])
            nav.quit()
        except:
            raise MyException("Unable to update the database")