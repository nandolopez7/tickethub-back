import datetime
import requests
import random

from bs4 import BeautifulSoup

# Models
from tickethub_back.events.models.events import Event


class WebScraping:

    def latiquetera(self):
        url = 'https://latiquetera.com/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        events = soup.find_all('div', class_='item-box-event')
        categories = Event.CategoryChoices.choices
        list_events = []
        
        for event in events:
            nombre = event.find('h3', class_='item-box-content-title').text.strip()
            info_fecha_str = event.find('div', class_='item-box-content-subtitle').text.strip()
            info_fecha_list = info_fecha_str.split("y")
            fecha_str = info_fecha_list[len(info_fecha_list)-1].replace('Viernes', '').replace('Lunes', '') \
                .replace('Martes', '').replace('Miércoles', '').replace('Jueves', '').replace('Sábado', '') \
                .replace('Domingo', '').replace('de', '').strip()
            date_event = self.convertir_fecha(fecha_str)
            place = event.find('span').text.strip()
            element_img = event.find('img')
            file_cover = url + element_img['src'] if element_img else ''
            category = str(random.choices(categories)[0][0]).lower().capitalize()

            detalles_evento = {
                'name': nombre,
                'date': date_event,
                'place': place,
                'file_cover': file_cover,
                'is_active': True,
                'time': datetime.time(0, 0),
                'category': category,
                'description': info_fecha_str,
            }
            print("*** detalles_evento: ", detalles_evento)
            
            if not Event.objects.filter(name=nombre).exists():  # Si el evento no existe, se crea
                event_obj = Event.objects.create(**detalles_evento)
                print("******** Creado: ", event_obj)
                list_events.append(detalles_evento)
            print('-' * 40)

        print(f'Total de nuevos eventos creados: {len(list_events)}')    
        return list_events

    def convertir_fecha(self, fecha_str):
        meses = {
            'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
            'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
            'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
        }
        try:
            partes_fecha = fecha_str.lower().split(' ')
            partes = [x for x in partes_fecha if x != '']
            dia, mes, anio = partes[0], meses[partes[1]], partes[2]
            fecha_format = f'{dia}-{mes}-{anio}'
            return datetime.datetime.strptime(fecha_format, '%d-%m-%Y')
        except Exception as e:
            print("** error fecha: ", e)
            return None
