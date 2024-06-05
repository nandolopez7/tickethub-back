import datetime
import requests


from bs4 import BeautifulSoup

# Models
from tickethub_back.events.models.events import Event

# URL de la página de eventos
url = 'https://latiquetera.com/'

# Obtener el contenido HTML de la página
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar todos los eventos
eventos = soup.find_all('div', class_='item-box-event')


# Lista para almacenar los detalles de los eventos
lista_eventos = []

meses = {
    'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
    'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
    'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
}

def convertir_fecha(fecha_str):
    try:
        partes_fecha = fecha_str.lower().split(' ')
        partes = [x for x in partes_fecha if x != '']
        dia = partes[0]
        mes = meses[partes[1]]
        anio = partes[2]
        fecha_format = f'{dia}-{mes}-{anio}'
        return datetime.datetime.strptime(fecha_format, '%d-%m-%Y')
    except Exception as e:
        print("** error fecha: ", e)
        return datetime.datetime.now().date()

# Imprimir los detalles de los eventos
for evento in eventos:
    nombre = evento.find('h3', class_='item-box-content-title').text.strip()
    info_fecha = evento.find('div', class_='item-box-content-subtitle').text.strip().split("y")
    fecha_str = info_fecha[len(info_fecha)-1].replace('Viernes', '').replace('Lunes', '') \
        .replace('Martes', '').replace('Miércoles', '').replace('Jueves', '').replace('Sábado', '') \
        .replace('Domingo', '').replace('de', '').strip()
    fecha_evento = convertir_fecha(fecha_str)
    lugar = evento.find('span').text.strip()
    element_img = evento.find('img')
    foto_url = "https://latiquetera.com/" + element_img['src'] if element_img else ''

    # Crear un diccionario con los detalles del evento
    detalles_evento = {
        'Nombre del evento': nombre,
        'Fecha': fecha_evento,
        'Lugar': lugar,
        'Foto URL': foto_url
    }
    print("*** detalles_evento: ", detalles_evento)
    
    # Dentro del bucle donde obtienes los detalles de cada evento

    if not Event.objects.filter(name=nombre).exists():  # Si el evento no existe, se crea
        evento = Event.objects.create(
            name=nombre,
            date=fecha_evento,
            time=datetime.time(0, 0),  # Puedes modificar esto para extraer la hora correcta
            place=lugar,
            file_cover=foto_url,
            is_active=True
        )
        print("******** Creado: ", evento)
        # Agregar el diccionario a la lista
        lista_eventos.append(detalles_evento)

    print('-' * 40)



print(f'Total de eventos: {len(lista_eventos)}')
