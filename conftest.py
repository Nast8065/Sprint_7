import pytest
import logging
from helps import Courier

logger = logging.getLogger(__name__)

@pytest.fixture()
def courier():
    courier_instance = Courier()  # Создаем один экземпляр класса Courier
    courier_create = courier_instance.courier_registration_in_the_system_and_get_courier_data()
    courier_login = courier_instance.courier_login_in_the_system_and_get_id_courier(courier_create["data"])
    yield courier_create
    courier_instance.courier_subsequent_deletion(courier_login["id"])


@pytest.fixture()
def courier_delete():
    courier_instance = Courier()  # Создаем один экземпляр класса Courier
    courier_create = courier_instance.courier_registration_in_the_system_and_get_courier_data()
    # logger.info(courier_create['data'])  # если необходимо логировать, тогда убрать print
    courier_login = courier_instance.courier_login_in_the_system_and_get_id_courier(courier_create["data"])
    return courier_login   # Используем return вместо yield

@pytest.fixture
def courier_fixture():
    """Фикстура для создания и удаления курьера."""
    courier_data = DataCourier.valid_data_login
    
    # Создаем курьера
    response = requests.post(f'{Urls.Yandex_scooter_URL}{Endpoints.create_courier}', data=courier_data)
    assert response.status_code == 201  # Проверяем успешное создание курьера

    # Получаем ID курьера для дальнейшего использования
    login_resp = requests.post(f'{Urls.Yandex_scooter_URL}{Endpoints.login_courier}', data=courier_data)
    assert login_resp.status_code == 200  # Проверяем успешный логин
    courier_id = login_resp.json().get("id")

    yield courier_id  # Возвращаем ID курьера для использования в тестах

    # Удаляем курьера после завершения теста
    requests.delete(f'{Urls.Yandex_scooter_URL}{Endpoints.delete_courier}{courier_id}')


