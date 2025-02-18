import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байтов
import requests
from PIL import Image
from GeoCode import get_ll, get_spn, get_org, get_distance

#toponym_to_find = " ".join(sys.argv[1:])
toponym_to_find = "Тольятти, Ворошилова 24"
toponym_longitude, toponym_lattitude = get_ll(toponym_to_find)
address_ll = f"{toponym_longitude},{toponym_lattitude}"
delta = "0.005,0.005"

organization = get_org(address_ll, delta, "аптека")
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]
org_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
org_point = f"{point[0]},{point[1]}"
apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": address_ll,
    "spn": delta,
    "apikey": apikey,
    # добавим точку, чтобы указать найденную аптеку
    "pt": f"{org_point},pm2dgl~{address_ll},pm2rdl"
}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()
a = (toponym_longitude,toponym_lattitude)
b = tuple(point)
distance = get_distance(a, b)
distance = f"Расстояние: \t{distance} км."
name = f"Название:\t{org_name}"
adress = f"Адрес: \t{org_address}"
time = f"Время работа: \t{org_time}"
print(name,adress,time,distance, sep="\n")
