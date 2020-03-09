# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
from pprint import pprint
import requests
import json

user_str = input('Введите username:')
main_link = f'https://api.github.com/users/{user_str}/repos'

response = requests.get(f'{main_link}')

if response.ok:
    data = json.loads(response.text)
    with open(f"repos_{user_str}.json", "w", encoding="utf-8") as file:
        json.dump(data, file)

    print('Репозитории пользователя:')
    for i in data:
        print(i['name'])

# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему,
# пройдя авторизацию. Ответ сервера записать в файл.

main_link = 'https://api.spaceinvoices.com/v1/organizations/5e65fdb5dd33e6362f634c5e'
params = {
    'access_token': 'uw4UE6S4bmyLLXE2HWbkJPbwyEFFuGtvtNeAI01xK5HD88rozSr144E410QJt2BN'
}

response = requests.get(f'{main_link}', params)

if response.ok:
    data = json.loads(response.text)
    with open(f"api_space.json", "w", encoding="utf-8") as file:
        json.dump(data, file)
    print(response.text)
