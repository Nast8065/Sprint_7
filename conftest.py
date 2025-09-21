import pytest
import logging
from helps import Courier

logger = logging.getLogger(__name__)

@pytest.fixture()
def courier():
    courier_create = Courier().courier_registration_in_the_system_and_get_courier_data()
    courier_login = Courier().courier_login_in_the_system_and_get_id_courier(courier_create["data"])
    yield courier_create
    Courier().courier_subsequent_deletion(courier_login["id"])

@pytest.fixture()
def courier_delete():
    courier_create = Courier().courier_registration_in_the_system_and_get_courier_data()
    # logger.info(courier_create['data'])  # если необходимо логировать, тогда убрать print
    courier_login = Courier().courier_login_in_the_system_and_get_id_courier(courier_create["data"])
    yield courier_login
