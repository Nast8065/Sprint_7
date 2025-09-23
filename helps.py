from faker import Faker
import requests

from endpoints import Endpoints
from urls import Urls


class CreatingCourier:
    # функция создания курьера с валидными несуществующими данными
    @step
    @staticmethod
    def creating_courier_fake_data():
        fake = Faker("ru_RU")
        login = fake.user_name()
        password = fake.password()
        firstname = fake.first_name()
        data = {
            "login": "login",
            "password": "password",
            "firstName": "firstname"
        }

        return data

    # функция создания курьера с не валидными данными без поля "Password"
    @step
    @staticmethod
    def creating_courier_invalid_data_without_password_field():
        fake = Faker("ru_RU")
        firstname = fake.first_name()
        password = fake.password()
        data = {
            "login": "login",
            "password": "",
            "firstName": "firstname"
        }

        return data

    # функция создания курьера с не валидными данными без поля "Login"
    @step
    @staticmethod
    def creating_courier_invalid_data_without_login_field():
        fake = Faker("ru_RU")
        login = fake.user_name()
        firstname = fake.first_name()
        data = {
            "login": "",
            "password": "password",
            "firstName": "firstname"
        }

        return data


class DataCourier:
    # валидные данные для регистрации
    valid_data_login = CreatingCourier.creating_courier_fake_data()

    # невалидные данные для регистрации без поля "Password"
    invalid_data_login_without_password = CreatingCourier.creating_courier_invalid_data_without_password_field()

    # невалидные данные для регистрации без поля "Login"
    invalid_data_login_without_login = CreatingCourier.creating_courier_invalid_data_without_login_field()

    # данные несуществующего курьера
    null_data_login = {
        "login": "test",
        "password": "test"
    }


class Courier:

    # функция регистрации в системе с возвратом ответа и данных курьера
    @staticmethod
    @step("Регистрация курьера в системе")
    def courier_registration_in_the_system_and_get_courier_data():
        data = CreatingCourier.generating_fake_valid_data_to_create_courier()
        response = requests.post(f'{Urls.Yandex_scooter_URL}{Endpoints.create_courier}', data=data)
        return {"response_text": response.text, "status_code": response.status_code, "data": data}

    # функция логина в системе с возвратом ответа и id курьера
    @staticmethod
    @step("Логин курьера в системе")
    def courier_login_in_the_system_and_get_id_courier(data):
        response = requests.post(f'{Urls.Yandex_scooter_URL}{Endpoints.login_courier}', data=data)
        return {"id": str(response.json()["id"]), "response_text": response.text, "status_code": response.status_code}

    # функция удаления курьера
    @staticmethod
    @step("Удаление курьера")
    def courier_subsequent_deletion(id):
        response = requests.delete(f'{Urls.Yandex_scooter_URL}{Endpoints.delete_courier}{id}')
        return {"response_text": response.text, "status_code": response.status_code}


class DataOrder:
    # данные для заказа самоката без цвета
    data = {
        "firstName": "Анастасия",
        "lastName": "Щавинская",
        "address": "г. Новосибирск",
        "metroStation": 1,
        "phone": "+7 906 996 8806",
        "rentTime": 4,
        "deliveryDate": "2025-09-22",
        "comment": "Осторожно, злая собака, а кот вообще псих",
    }
