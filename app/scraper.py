from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def search_info(title):
    driver = webdriver.Chrome()

    url = "https://www.honda.com.br/motos/modelos" 
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 1)
        infos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "single-product")))
            
        for info in infos:
            motoTitle = info.find_element(By.CLASS_NAME, "title").text
            price = info.find_element(By.CLASS_NAME, "price").text

            if title.lower() in motoTitle.lower():
                driver.quit()
                return price
            
    except Exception as error:
        print("Erro na busca", error)

    finally:
        driver.quit()
    
    return None
