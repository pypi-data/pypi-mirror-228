import requests
import configparser
from typing import Self
from passwordless_types import UserVerification, AuthenticatorType,responseType
from exceptions import ApiSecretInvalidError,InvalidTokenError
import exceptions



class PasswordlessClient:
    def __init__(self, config:dict):
        if config:
            self.API_URL = config["API"]["API_URL"]
            self.API_SECRET = config["API"]["API_SECRET"]
            self.API_KEY = config["API"]["API_KEY"]
            self.VERIFY = config["API"]["VERIFY"]
        else:
            # Read API configurations from the config file
            config = configparser.ConfigParser()
            config.read("passwordlessconfig.ini")
            self.API_URL = config["API"]["API_URL"]
            self.API_SECRET = config["API"]["API_SECRET"]
            self.API_KEY = config["API"]["API_KEY"]
            self.VERIFY = config["API"].getboolean("VERIFY")
            self.headers = {
                "ApiSecret": self.API_SECRET,
                "Api-Key": self.API_KEY,
                "Content-Type": "application/json",
            }

    def register_token(
        self: Self,
        user_id: str,
        username: str,
        displayname: str,
        authenticator_type: AuthenticatorType = "any",
        user_verification: UserVerification = "preferred",
        aliases: list[str] = [],
        alias_hashing: bool = True,
    ):
        payload = {
            "userId": user_id,
            "username": username,
            "displayname": displayname,
            "authenticatorType": authenticator_type,
            "userVerification": user_verification,
            "aliases": aliases,
            "aliasHashing": alias_hashing,
        }
        try: 
            return self._make_request("register/token", payload)
        except Exception as e:
            if "A valid \u0027ApiSecret\u0027 header is required." in e.title:
                raise ApiSecretInvalidError(e.type, e.title, e.status, e.detail, e.message)

    def signin_verify(self: Self, token: str):
        payload = {"token": token}
        try:
            return self._make_request("signin/verify", payload)
        except Exception as e:
            if not e.token.startswith("verify_"):
                raise InvalidTokenError(e.status)

    def alias(self: Self, user_id: str, aliases: list[str] = [], hashing: bool = True):
        payload = {"userId": user_id, "aliases": aliases, "hashing": hashing}
        return self._make_request("alias", payload)

    def credentials_list(self: Self, user_id: str):
        payload = {"userId": user_id}
        return self._make_request("credentials/list", payload)

    def credentials_delete(self: Self, credential_id: str):
        payload = {"credentialId": credential_id}
        return self._make_request("credentials/delete", payload)

    def _make_request(self: Self, endpoint: str, payload: dict):
        # General method to make requests
        response = requests.post(
            f"{self.API_URL}/{endpoint}",
            verify=self.VERIFY,
            json=payload,
            headers=self.headers,
        )
        if response.ok:
            try:
                resp=responseType(response.json(), response.status_code)
                return resp
            except Exception as e:
                c=e.args
                exceptions.sample(c)
                
                
        else:
            raise Exception(
                f"Failed to fetch response successfully. Status Code: {response.status_code}\n{response.text}"
            )
