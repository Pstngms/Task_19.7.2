import json

from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# !!!Самостоятельная работа!!!
# 1
def test_add_new_pet_without_photo_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                                   age='4'):
    """Проверяем что можно добавить питомца без фотографии с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фотографии
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''


# 2
def test_add_pet_photo(pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавления фотографии питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового без фото и запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Берём id первого питомца из списка и отправляем запрос на добавление фото

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа равен 200 и у питомца есть фото
    assert status == 200
    assert result['pet_photo'] != ''


# 3
def test_get_api_key_for_incorrect_user(email=invalid_email, password=invalid_password):
    """ Проверяем что запрос api ключа с некорректными данными возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
    status, _ = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


# 4
def test_add_new_pet_with_incorrect_age(name='Барбоскин', animal_type='двортерьер',
                                        age='HELLO!!!', pet_photo='images/cat1.jpg'):
    """Проверяем что добавление питомца с некорректным возрастом возвращает статус ошибки"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем что статус ответа не равен 200
    assert status != 200


# 5
def test_add_new_pet_without_data(name=None, animal_type=None,
                                  age=None):
    """Проверяем что добавление питомца с пустыми значениями возвращает статус ошибки"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, _ = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Проверяем что статус ответа не равен 200
    assert status != 200


# 6
def test_add_new_pet_with_incorrect_auth_key(name='Барбоскин', animal_type='двортерьер',
                                             age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что добавление питомца с неверным auth_key возвращает статус 403"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Создаём неверный ключ api и сохраняем в переменную auth_key
    incorrect_auth_key = '{"key": "1234"}'
    auth_key = json.loads(incorrect_auth_key)

    # Добавляем питомца
    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


# 7
def test_add_file_instead_of_photo(pet_photo='images/file.txt'):
    """Проверяем что добавление неверного файла вместо фото возвращает статус ошибки"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового без фото и запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь файла питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Берём id первого питомца из списка и отправляем запрос на добавление фото

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа не равен 200
    assert status != 200


# 8
def test_delete_pet_with_incorrect_auth_key():
    """Проверяем что удаление питомца с неверным auth_key возвращает статус 403"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']

    # Создаём неверный ключ api и сохраняем в переменную auth_key
    incorrect_auth_key = '{"key": "1234"}'
    auth_key = json.loads(incorrect_auth_key)

    # Отправляем запрос на удаление
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


# 9
def test_get_all_pets_with_incorrect_filter(filter='Hello '):
    """ Проверяем что запрос всех питомцев с несуществующим значением filter возвращает статус ошибки.

    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.get_list_of_pets(auth_key, filter)

    # Проверяем что статус ответа не равен 200
    assert status != 200


# 10
def test_get_all_pets_with_incorrect_key(filter=''):
    """ Проверяем что запрос всех питомцев с неверным auth_key возвращает статус 403.

    Доступное значение параметра filter - 'my_pets' либо '' """

    # Создаём неверный ключ api и сохраняем в переменную auth_key
    incorrect_auth_key = '{"key": "1234"}'
    auth_key = json.loads(incorrect_auth_key)

    status, _ = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
