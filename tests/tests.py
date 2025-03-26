import pytest
import allure


@allure.title("Регистрация нового пользователя")
def test_register_success(auth_api, random_user):
    with allure.step("Отправляем запрос POST /auth/register"):
        response = auth_api.register(email=random_user["email"], password=random_user["password"])

    with allure.step("Проверяем, что возвращается 200 статус код"):
        assert response.status_code == 200, f"Пользователь не зарегистрирован.Получен статус код {response.status_code}"


@allure.title("Регистрация пользователя с уже существующим email")
def test_register_existing_email(auth_api, registered_user):
    with allure.step("Отправляем запрос POST /auth/register с уже зарегистрированным email"):
        response = auth_api.register(email=registered_user["email"], password=registered_user["password"])

    with allure.step("Проверяем, что возвращается статус код 409 с тектом"):
        assert response.status_code == 409, f"Ожидался статус код 409, получен {response.status_code}"
        assert response.json() == {"detail": "User already exists"}, f"Получен другой текст ответа {response.json()}"


@allure.title("Регистрация пользователя с пустым паролем и email")
def test_register_empty_credentials(auth_api):
    with allure.step("Отправляем запрос POST /auth/register с пустыми полями для email и пароля"):
        response = auth_api.register(email="", password="")

    with allure.step("Проверяем, что возвращается статус код 422"):
        assert response.status_code == 422, f"Ожидался статус код 422, получен {response.status_code}"


@allure.title("Регистрация с максимальной длиной email/пароля")
def test_register_max_length_email_password(auth_api):
    max_email = "a" * 254 + "@example.com"
    max_password = "a" * 128

    with allure.step(f"Отправляем запрос POST /auth/register с максимальной длиной email: {max_email}, \
                    пароля: {max_password}"):
        response = auth_api.register(email=max_email, password=max_password)

    with allure.step("Проверяем, что возвращается статус код 422"):
        assert response.status_code == 422, f"Ожидался статус код 422, получен {response.status_code}"


@pytest.mark.parametrize("email", ["user@example", "userexample.ru", "userexample.com"])
@allure.title("Регистрация с некорректными emails")
def test_register_invalid_email_format(auth_api, email):
    with allure.step(f"Отправляем запрос POST /auth/register с некорректным email: {email}"):
        response = auth_api.register(email=email, password="Password123!")

    with allure.step("Проверяем, что возвращается статус код 422"):
        assert response.status_code == 422, f"Ожидался статус код 422, получен {response.status_code}"


@allure.title("Успешный вход пользователя")
def test_login_success(auth_api, registered_user):
    with allure.step("Отправляем запрос POST /auth/login с валидными данными"):
        response = auth_api.login(email=registered_user["email"], password=registered_user["password"])

    with allure.step("Проверяем, что возвращается 200 статус код"):
        assert response.status_code == 200, f"Ожидался статус код 200, получен {response.status_code}"

    with allure.step("Проверяем, что в ответе есть access_token"):
        assert "access_token" in response.json(), "В ответе отсутствует access_token"


@allure.title("Вход с несуществующим email")
def test_login_nonexistent_email(auth_api):
    with allure.step("Отправляем запрос POST /auth/login с несуществующим email"):
        response = auth_api.login(email="nonexistent@example.com", password="Password123!")

    with allure.step("Проверяем, что возвращается статус код 401 с тектом"):
        assert response.status_code == 401, f"Ожидался статус код 401, получен {response.status_code}"
        assert response.json() == {"detail": "Incorrect email or password"}, f"Получен другой текст ответа \
                                    {response.json()}"


@allure.title("Вход с неверным паролем")
def test_login_wrong_password(auth_api, registered_user):
    with allure.step("Отправляем запрос POST /auth/login с неверным паролем"):
        response = auth_api.login(email=registered_user["email"], password="WrongPassword123!")

    with allure.step("Проверяем, что возвращается статус код 401 с тектом"):
        assert response.status_code == 401, f"Ожидался статус код 401, получен {response.status_code}"
        assert response.json() == {"detail": "Incorrect email or password"}, f"Получен другой текст ответа \
                                    {response.json()}"


@allure.title("Попытка входа с XSS-скриптом в email")
def test_login_xss_in_email(auth_api):
    with allure.step("Отправляем запрос POST /auth/login с XSS-скриптом в email"):
        response = auth_api.login(email="<script>alert('XSS')</script>user@example.com", password="Password123!")

    with allure.step("Проверяем, что возвращается статус код 422 с тектом"):
        assert response.status_code == 422, f"Ожидался статус код 422, получен {response.status_code}"


@allure.title("Выход пользователя")
def test_logout_success(auth_api, logged_in_user):
    access_token = logged_in_user["access_token"]

    with allure.step("Отправляем запрос POST /auth/logout"):
        response = auth_api.logout(access_token)

    with allure.step("Проверяем, что возвращается 200 статус код"):
        assert response.status_code == 200, f"Ожидался статус код 200, получен {response.status_code}"


@allure.title("Получение информации о текущем пользователе")
def test_get_current_user_success(auth_api, logged_in_user):
    access_token = logged_in_user["access_token"]

    with allure.step("Отправляем запрос GET /auth/current_user"):
        response = auth_api.get_current_user(access_token)
        result = response.json()
    with allure.step("Проверяем, что возвращается 200 статус код"):
        assert response.status_code == 200, f"Ожидался статус код 200, получен {response.status_code}"

    with allure.step("Проверяем, что email в ответе соответствует ожидаемому"):
        assert result["email"] == logged_in_user["email"], f"Email в ответе {result["email"]} \
                                                не соответствует ожидаемому {logged_in_user["email"]}"


@allure.title("Получение данных текущего пользователя без авторизационного токена")
def test_get_current_user_without_token(auth_api):
    with allure.step("Отправляем запрос GET /auth/current_user без токена"):
        response = auth_api.get_current_user(access_token="")

    with allure.step("Проверяем, что возвращается статус код 401 с тектом"):
        assert response.status_code == 401, f"Ожидался статус код 401, получен {response.status_code}"
        assert response.json() == {"detail": "Authentication token is missing"}, f"Получен другой текст ответа \
                                    {response.json()}"


@allure.title("Получение списка всех пользователей обычным юзером")
def test_get_all_users_as_normal_user(auth_api, logged_in_user):
    with allure.step("Отправка GET-запроса к /auth/users_all как обычный пользователь"):
        response = auth_api.get_all_users(logged_in_user)

    with allure.step("Проверяем, что возвращается статус код 403 с тектом"):
        assert response.status_code == 403, f"Ожидался статус код 403, получен {response.status_code}"
        assert response.json() == {"detail": "You are not an admin"}, f"Получен другой текст ответа {response.json()}"
