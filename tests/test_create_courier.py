import allure
import pytest
import requests
from helps import DataCourier
from endpoints import Endpoints
from urls import Urls

class TestCreateCourier:

    @allure.title('Проверка создания нового курьера')
    @allure.description('Отправляем запрос на создание курьера, проверяем ответ и удаляем созданного курьера')
    def test_registration_courier_success(self):
        with allure.step("Генерируем валидные данные для курьера"):
            courier_data = DataCourier.valid_data_login
        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post(f'{Urls.Yandex_Scooter_URL}{Endpoints.create_courier}', data=courier_data)
        with allure.step("Проверяем успешный статус и ответ от сервера"):
            assert response.status_code ==201
            assert response.text == '{"ok":true}'
        with allure.step("Логинимся для получения ID"):
            login_resp = requests.post(f'{Urls.Yandex_Scooter_URL}{Endpoints.login_courier}', data=courier_data)
            courier_id = login_resp.json().get("id")
        with allure.step("Удаляем созданного курьера"):
            requests.delete(f'{Urls.Yandex_Scooter_URL}{Endpoints.delete_courier}{courier_id}')

    @allure.title('Проверка ошибки при создании двух одинаковых курьеров')
    @allure.description('Отправляем повторный запрос на создание курьера, проверяем ответ и удаляем курьера')
    def test_registration_double_courier_failed(self):
        with allure.step("Генерируем валидные данные для курьера"):
            courier_data = DataCourier.valid_data_login
        with allure.step("Первый запрос на создание курьера"):
            requests.post(f'{Urls.Yandex_Scooter_URL}{Endpoints.create_courier}', data=courier_data)
        with allure.step("Второй запрос на создание курьера с теми же данными"):
            response = requests.post(f'{Urls.Yandex_Scooter_URL}{Endpoints.create_courier}', data=courier_data)
        with allure.step("Проверяем, что код ответа 409 и присутствует сообщение об ошибке"):
            assert response.status_code == 409
            assert "Этот логин уже используется" in response.text
        with allure.step("Логинимся для удаления курьера"):
            login_resp = requests.post(f'{Urls.Yandex_Scooter_URL}{Endpoints.login_courier}', data=courier_data)
            courier_id = login_resp.json().get("id")
        with allure.step("Удаляем курьера"):
            requests.delete(f'{Urls.Yandex_Scooter_URL}{Endpoints.delete_courier}{courier_id}')

    @allure.title('Проверка ошибки при создании курьера без обязательных полей')
    @allure.description('Отправляем запрос без обязательных полей и проверяем ошибку')
    @pytest.mark.parametrize('courier_data', [
        DataCourier.invalid_data_login_without_login,
        DataCourier.invalid_data_login_without_password
    ])
    def test_courier_registration_without_parameters_failed(self, courier_data):
        with allure.step("Отправляем запрос с неполными данными"):
            response = requests.post(f'{Urls.Yandex_Scooter_URL}{Endpoints.create_courier}', data=courier_data)
        with allure.step("Проверяем, что получаем ошибку 400 и сообщение о нехватке данных"):
            assert response.status_code == 400
            assert "Недостаточно данных для создания учетной записи" in response.text
