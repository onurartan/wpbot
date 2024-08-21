#  --------- Whatsapp Message sending bot was created by onur artan ---------  #


import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Import streamlit
import streamlit as st


logging.basicConfig(
    filename="bot_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

WHATSAPP_WEB_URL = "https://web.whatsapp.com/"


def run_bot(groups, message):
    try:
        user_profile = os.getenv("USERPROFILE")
        chrome_profile_path = os.path.join(
            user_profile, r"AppData\\Local\\Microsoft\\Google\\User Data"
        )
        
        
        #  --------- Driver Options ---------  #
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-data-dir={chrome_profile_path}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        
        
        #  --------- Setup Driver ---------  #
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

        driver.get(WHATSAPP_WEB_URL)

        st.info("Lütfen Whatsapp Web'e giriş yapın ve QR kodunu taratın..."),
        time.sleep(20)
        
        
        #  --------- Bütün Gruplara Mesajı İlet ---------  #
        for group in groups:
            search_box = None
            try:
                #  --------- Arama Kutusunu Bul ---------  #
                search_box = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//div[@contenteditable="true" and @data-tab="3"]')
                    )
                )
                search_box.clear()
                search_box.send_keys(group)
                time.sleep(2)

                group_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f'//span[@title="{group}"]')
                    )
                )
                group_element.click()
                
                
                
                 #  --------- Mesaj Kutusunu Bul ---------  #
                message_box = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//div[@contenteditable="true" and @data-tab="10"]')
                    )
                )
                message_box.clear()
                message_box.send_keys(message.replace("[group_name]", group))
                message_box.send_keys(Keys.ENTER)
                time.sleep(4)

                st.success(f"Mesaj başarıyla '{group}' grubuna iletildi.")
                logging.info(f"Mesaj başarıyla '{group}' grubuna iletildi.")

            except Exception as e:
                error_message = str(e)
                logging.error(f"Grup '{group}' için hata: {error_message}")
                if (
                    "NoSuchElementException" in error_message
                    or "TimeoutException" in error_message
                ):
                    st.error(
                        f"'{group}' grubuna ulaşılamadı. Grubun doğru adını yazdığınızdan emin olun."
                    )
                else:
                    st.error(f"Bir hata oluştu: {error_message}")

    except Exception as e:
        logging.error(f"Bot çalıştırılırken bir hata oluştu: {e}")
        st.error(f"Bot çalıştırılırken bir hata oluştu: {e}")

    finally:
        if driver:
            driver.quit()
