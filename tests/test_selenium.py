from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Inicia el navegador
driver = webdriver.Chrome()

# Abre tu sistema (puede ser local o deployado)
driver.get("http://127.0.0.1:5500/index.html")

# Espera que cargue
time.sleep(2)

# Verifica el título o un elemento
assert "Sistema de Información de Tutorías" in driver.title

# Busca un botón o campo
boton = driver.find_element(By.TAG_NAME, "button")
print("Botón encontrado:", boton.text)

driver.quit()
