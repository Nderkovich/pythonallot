import unittest
import random
import requests
import string

url = "https://petstore.swagger.io/v2/user"


def random_string():
    return "".join(random.choices(string.ascii_lowercase, k=16))


def generate_payload():
    return {
        "id": 0,
        "username": random_string(),
        "firstName": random_string(),
        "lastName": random_string(),
        "email": "mail@example.com",
        "password": random_string(),
        "phone": "11123131",
        "userStatus": 0
    }


class UserCreationTest(unittest.TestCase):

    def setUp(self):
        self.payload = generate_payload()

    def test_create_user(self):
        response = requests.post(url, json=self.payload)
        self.assertEqual(response.status_code, requests.codes["ok"])

    def test_create_user_with_array(self):
        response = requests.post(
            url + "/createWithArray", json=[self.payload, generate_payload()])
        self.assertEqual(response.status_code, requests.codes["ok"])

    def test_get_created_user(self):
        create_response = requests.post(url, json=self.payload)
        self.assertEqual(create_response.status_code, requests.codes["ok"])
        username = self.payload["username"]
        get_response = requests.get(url + f"/{username}")
        self.assertEqual(get_response.json()["firstName"], self.payload["firstName"])


class UserSessionTest(unittest.TestCase):

    def setUp(self):
        self.payload=generate_payload()
        create_response=requests.post(url, json=self.payload)
        create_response.raise_for_status()
        self.payload["id"]=int(create_response.json()["message"])

        # login user
        self.session=requests.Session()
        username, password=self.payload["username"], self.payload["password"]
        self.session.get(
            url + f"/login?username={username}&password={password}").raise_for_status()

    def test_user_update(self):
        update_payload=self.payload
        update_payload["firstName"]=random_string()
        username=update_payload["username"]
        update_response=self.session.put(
            url + f"/{username}", json=update_payload)
        self.assertEqual(update_response.status_code, requests.codes["ok"])
        response=requests.get(url + f"/{username}")
        self.assertEqual(
            response.json()["firstName"], update_payload["firstName"])

    def test_user_delete(self):
        username=self.payload["username"]
        response=self.session.delete(url + f"/{username}")
        self.assertEqual(response.status_code, requests.codes["ok"])

    def test_logout(self):
        response = self.session.get(url + "/logout")
        self.assertEqual(response.status_code, requests.codes["ok"])


if __name__ == "__main__":
    unittest.main()
