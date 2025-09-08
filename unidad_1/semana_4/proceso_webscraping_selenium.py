# Juarez Ramirez Steve
# Grupo 952
# Web-scraping de Ebay utilizando Selenium

# Se importan los modulos necesarios para el web-scraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Se crea funcion para navegar ebay y tomar capturas de pantalla
def ebay_search(search, num_paginas=1):
    service = Service(ChromeDriverManager().install())
    opc = Options()
    opc.add_argument("--window-size=1020x1200")
    navegador = webdriver.Chrome(service=service, options=opc)
    navegador.get("https://ebay.com")
  # Se crea carpeta "screenshots" de forma automatica en caso de que no exista
    os.makedirs("screenshots", exist_ok=True)

    WebDriverWait(navegador, 5).until(
        EC.presence_of_element_located((By.ID, "gh-ac"))
    )
    input_element = navegador.find_element(By.ID, "gh-ac")
    input_element.send_keys(search + Keys.ENTER)

    # Se inicia ciclo para recorrer la cantidad de paginas solicitadas
    for pagina in range(1, num_paginas + 1):
        # Espera a que carguen los resultados
        WebDriverWait(navegador, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-item"))
        )

        # Se utiliza f-string para guardar capturas con nombre especifico
        navegador.save_screenshot(f"screenshots/ebay_{search}_{pagina}.png")
        time.sleep(2)

        if pagina < num_paginas:
            try:
                next_page = WebDriverWait(navegador, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.pagination__next"))
                )
                next_page.click()
                time.sleep(2)
            # Manejo de excepciones
            except:
                print("No existen más páginas disponibles.")
                break

    navegador.quit()

# Se crea funcion para llevar a cabo el scraping
# Por medio de consola se le pregunta al usuario el producto y las paginas a explorar
if __name__ == '__main__':
    producto = input("Ingresa el producto a buscar: ")
    num_paginas = int(input("Ingresa la cantidad de paginas a explorar: "))
    ebay_search(producto, num_paginas)
