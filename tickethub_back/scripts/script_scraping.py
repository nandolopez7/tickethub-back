import datetime
import sys
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
import django
django.setup()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from tickethub_back.events.models.events import Event
from tickethub_back.events.serializers.events import EventSerializer

import time

# Configurar Selenium para usar Chrome en Google Colab
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Ejecutar en modo headless (sin ventana)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Ruta al ejecutable de ChromeDriver
chromedriver_path = "/usr/lib/chromium-browser/chromedriver"

# Crear una instancia de Chrome WebDriver
# Create a Chrome WebDriver instance
driver = webdriver.Chrome(options=options)

# URL de la página de eventos
url = 'https://www.tuboleta.com/eventos/recomendados'

# Abrir la página en el navegador controlado por Selenium
driver.get(url)

# Esperar a que la página se cargue completamente
time.sleep(5)

# Limitar el número de clics a 5 veces
clicks = 0
max_clicks = 8


while clicks < max_clicks:
    try:
        # Esperar a que el botón de "Cargar más eventos" sea clicable y luego hacer clic
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "CARGAR MÁS EVENTOS")]'))
        )
        load_more_button.click()
        # Esperar un poco para que se carguen los nuevos eventos
        time.sleep(5)
        clicks += 1
    except:
        # Si no se encuentra el botón o ya no se puede hacer clic, salir del bucle
        break

# Crear el objeto BeautifulSoup con el HTML de la página cargada por Selenium
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Encontrar todos los eventos
eventos = soup.find_all('div', class_='event')

# Lista para almacenar los detalles de los eventos
lista_eventos = []

# Imprimir los detalles de los eventos
contador = 0
if eventos:
    for evento in eventos:
        nombre = evento.find('h3').text.strip()
        fecha_dia = evento.find('div', class_='day').text.strip()
        fecha_mes_anio = evento.find('div', class_='content-date').text.strip().replace(fecha_dia, '').strip()
        lugar = evento.find('div', class_='title-place').text.strip()
        foto_url = evento.find('div', class_='header-event')['style'].split('url("')[1].split('");')[0]

        contador += 1
        # Crear un diccionario con los detalles del evento
        detalles_evento = {
            'nombre': nombre,
            'fecha': f'{fecha_dia} {fecha_mes_anio}',
            'lugar': lugar,
            'foto_url': foto_url
        }

        # Dentro del bucle donde obtienes los detalles de cada evento
        fecha_str = f'{fecha_dia} {fecha_mes_anio}'
        fecha_evento = datetime.datetime.strptime(fecha_str, '%d %b %Y')
        
        if not Event.objects.filter(name=nombre).exists():  # Si el evento no existe, se crea
            evento= Event.objects.create(
                        name=nombre,
                        date=fecha_evento,
                        time=datetime.time(0, 0),  # Puedes modificar esto para extraer la hora correcta
                        place=lugar,
                        file_cover=foto_url,
                        is_active=True
                    )
        
            evento.save()

            print(evento)
            # Agregar el diccionario a la lista
            lista_eventos.append(detalles_evento)

# Imprimir los detalles de los eventos
for evento in lista_eventos:
    print(f'Nombre del evento: {evento["nombre"]}')
    print(f'Fecha: {evento["fecha"]}')
    print(f'Lugar: {evento["lugar"]}')
    print(f'Foto URL: {evento["foto_url"]}')
    print('-' * 40)

print(f'Total de eventos: {len(lista_eventos)}')


# Cerrar el navegador controlado por Selenium
driver.quit()
