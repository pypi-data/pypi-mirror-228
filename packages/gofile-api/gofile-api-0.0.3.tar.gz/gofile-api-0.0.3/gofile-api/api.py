from requests.exceptions import RequestException
from typing import Iterable, NoReturn, Literal
from os.path import split as file_path_split
from requests import post, put, get
from random import choices


class GoFileSession:
    """class for communicating with the gofile api"""

    def __init__(
        self, max_retries: int = 5, raw_output: bool = False, token: str | None = None
    ) -> None:
        self.__max_retries = max_retries
        self.__retry_count = 0
        if token == None:
            self.__token = self.create_account()
        self.__root_folder: str = self.get_account_details()["rootFolder"]
        self.__raw = raw_output

    def get_server(self, raw: bool | None = None) -> str | dict:
        if raw == None:
            raw = self.__raw
        try:
            response = get("https://api.gofile.io/getServer")
        except RequestException:
            self.__next_retry()
            return self.get_server()
        if response.status_code == 200:
            if raw:
                return response.json()
            return response.json()["data"]["server"]
        else:
            self.__next_retry()
            return self.get_server(raw)

    def upload_file(
        self, file_path: str, raw: bool | None = None, folder_id: str | None = None
    ) -> str | dict:
        if raw == None:
            raw = self.__raw
        params = {"token": self.__token}
        if folder_id == None:
            params["folderId"] = folder_id
        else:
            params["folderId"] = self.__root_folder
        with open(file_path, "r") as file_opened:
            response = post(
                f"https://{self.get_server()}.gofile.io/uploadFile",
                params=params,
                files={file_path_split(file_path)[1]: file_opened},
            )
            if response.status_code == 200:
                if raw:
                    return response.json()
                return response.json()["data"]["downloadPage"]
            else:
                self.__next_retry()
                return self.upload_file(file_path, raw, folder_id)

    def get_content(
        self, content_id: str, raw: bool | None = None
    ) -> list[str] | bytes | dict:
        if raw == None:
            raw = self.__raw
        params = {"token": self.__token, "contentId": content_id}
        response = get("https://api.gofile.io/getContent", params=params)
        if response.status_code == 200:
            self.__reset_retry_count()
            if raw:
                return response.json()
            data = response.json()["data"]
            childs = data["childs"]
            if len(childs) != 1:
                return childs
            else:
                return get(data["contents"][childs[0]]["directLink"]).content

    def create_account(self, raw: bool | None = None) -> str:
        if raw == None:
            raw = self.__raw
        response = get("https://api.gofile.io/createAccount")
        if response.status_code == 200:
            if raw:
                return response.json()
            else:
                return response.json()["data"]["token"]
        else:
            self.__next_retry()
            return self.create_account(raw)

    def create_folder(
        self,
        folder_name: str | None = None,
        parent_folder_id: str | None = None,
        public: bool = True,
        folder_password: str | None = None,
        expiration_timestamp: float | None = None,
        description: str | None = None,
        tags: Iterable[str] | None = None,
    ) -> None:
        if parent_folder_id == None:
            parent_folder_id = self.__root_folder
        if folder_name == None:
            folder_name = "".join(choices("abcdefghijklmnopqrstuvwxyz1234567890", k=5))
        params = {
            "token": self.__token,
            "folderName": folder_name,
            "parentFolderId": parent_folder_id,
        }
        response = put("https://api.gofile.io/createFolder", params=params)
        if response.status_code == 200:
            response_json = response.json()
            data = response_json["data"]
            content_id = data["id"]
            self.set_option(content_id, "public", public)
            if folder_password != None:
                self.set_option(content_id, "password", folder_password)
            if expiration_timestamp != None:
                self.set_option(content_id, "expire", expiration_timestamp)
            if tags != None:
                self.set_option(content_id, "tags", tags)
            if description != None:
                self.set_option(content_id, "description", description)
        else:
            self.__next_retry()
            return self.create_folder(folder_name, parent_folder_id)

    def get_account_details(self, raw: bool | None = None) -> dict:
        if raw == None:
            raw = self.__raw
        params = {"token": self.__token}
        response = get("https://api.gofile.io/getAccountDetails", params=params)
        if response.status_code == 200:
            if raw:
                return response.json()
            return response.json()["data"]
        else:
            self.__next_retry()
            return self.get_account_details(raw)

    def copy_content(self, sources: Iterable[str], destination: str) -> None:
        """*sources*: Iterable of source content IDs\n
        *destination*: Content ID of destination folder"""
        sources_string = ",".join(sources)
        params = {
            "token": self.__token,
            "contentsId": sources,
            "folderIdDest": sources_string,
        }
        response = put("https://api.gofile.io/copyContent", params=params)
        if response.status_code != 200:
            self.__next_retry()
            return self.copy_content(sources, destination)

    def set_option(
        self,
        content_id: str,
        option_type: Literal[
            "public", "password", "description", "expire", "tags", "directLink"
        ],
        value: bool | str | float | int | Iterable[str],
    ) -> None:
        """For option_type "public", value must be a `bool`. The content_id must be a folder.\n
        For option_type "password", value must be a `str`. The content_id must be a folder.\n
        For option_type "description", value must be a `str`. The content_id must be a folder.\n
        For option_type "expire", value must be a `float` or an `int`. The content_id must be a folder.\n
        For option_type "tags", value must be an `Iterable[str]`. The content_id must be a folder.\n
        For option_type "directLink", value must be a `bool`. The content_id must be a file.\n
        """
        if option_type in ("public", "directLink"):
            if value:
                value = "true"
            else:
                value = "false"
        if option_type == "tags":
            value = ",".join(value)
        params = {
            "token": self.__token,
            "contentId": content_id,
            "option": option_type,
            "value": value,
        }
        response = put("https://api.gofile.io/setOption", params=params)
        if response.status_code != 200:
            self.__next_retry()
            return self.set_option(content_id, option_type, value)

    def set_token(self, new_token: str) -> None:
        self.__token = new_token
        self.__refresh_account_info()

    def reset_account(self) -> None:
        self.__token = self.create_account()
        self.__refresh_account_info()

    def __reset_retry_count(self) -> None:
        self.__retry_count = 0

    def __increase_retry_count(self, amount: int = 1) -> None:
        self.__retry_count += amount

    def __next_retry(self) -> None:
        if self.__retry_count == self.__max_retries:
            self.__reset_retry_count()
            self.__raise_max_retries()
        self.__increase_retry_count()

    def __refresh_account_info(self) -> None:
        account_details = self.get_account_details()
        self.__root_folder: str = account_details["rootFolder"]
        self.__tier: str = account_details["tier"]

    @staticmethod
    def __raise_max_retries() -> NoReturn:
        raise TimeoutError("max retries hit")

    @property
    def max_retries(self) -> int:
        return self.__max_retries

    @property
    def token(self) -> str:
        return self.__token

    @property
    def root_folder(self) -> str:
        return self.__root_folder

    @property
    def raw(self) -> bool:
        return self.__raw

    @property
    def tier(self) -> str:
        return self.__tier

    @property
    def is_guest(self) -> bool:
        return self.__tier == "guest"

    @property
    def is_standard(self) -> bool:
        return self.__tier == "standard"

    @property
    def is_premium(self) -> bool:
        return self.__tier == "premium"
