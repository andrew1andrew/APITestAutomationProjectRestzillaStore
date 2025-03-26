from requests import Session, Response


BASE_URL = 'https://restzilla.store'


class AuthAPI:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = Session()

    def register(self, email: str, password: str) -> Response:
        url = f"{self.base_url}/auth/register"
        data = {"email": email, "password": password}
        return self.session.post(url=url, json=data)

    def login(self, email: str, password: str) -> Response:
        url = f"{self.base_url}/auth/login"
        data = {"email": email, "password": password}
        return self.session.post(url=url, json=data)

    def logout(self, access_token: str) -> Response:
        url = f"{self.base_url}/auth/logout"
        headers = {"Authorization": f"{access_token}"}
        return self.session.post(url=url, headers=headers)

    def get_current_user(self, access_token: str) -> Response:
        url = f"{self.base_url}/auth/current_user"
        headers = {"Authorization": f"{access_token}"}
        return self.session.get(url=url, headers=headers)

    def get_all_users(self, admin_token: str) -> Response:
        url = f"{self.base_url}/auth/users_all"
        headers = {"Authorization": f"Bearer {admin_token}"}
        return self.session.get(url=url, headers=headers)
