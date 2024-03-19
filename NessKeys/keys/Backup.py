from ..JsonChecker.Checker import JsonChecker
from ..JsonChecker.exceptions.LeafBuildException import LeafBuildException
from ..interfaces.NessKey import NessKey
import json

class Backup(NessKey):

    __files_id = ""
    __dirs_id = ""
    __cipher = "aes"

    def load(self, keydata: dict):
        map = {
            "filedata": {
                "vendor": "Privateness",
                "type": "backup",
                "for": "backup"
            },
            "type": str,
            "address": str,
            "cipher": str,
            "seed": str,
            "key": str,
            "files_id": str,
            "dirs_id": str
        }

        JsonChecker.check('Backup key check', keydata, map)

        self.__seed = keydata["seed"]
        self.__key = keydata["key"]

        self.__files_id = keydata["files_id"]
        self.__dirs_id = keydata["dirs_id"]

        self.__type = keydata["type"]
        self.__address = keydata["address"]
        self.__cipher = "aes"
    
    def compile(self) -> dict:

        return {
            "filedata": {
                "vendor": "Privateness",
                "type": "backup",
                "for": "backup"
            },
            "type": self.__type,
            "address": self.__address,
            "cipher": self.__cipher,
            "seed": self.__seed,
            "key": self.__key,
            "files_id": self.__files_id,
            "dirs_id": self.__dirs_id
        }

    def serialize(self) -> str:
        return json.dumps(self.compile())

    def print(self):
        return "Privateness backup"

    def getFilename(self):
        return "backup.key.json"
    
    def worm(self):
        return ''
    
    def nvs(self):
        return ''

    def getSeed(self):
        return self.__seed

    def getKey(self):
        return self.__key

    def getType(self):
        return self.__type

    def getAddress(self):
        return self.__address

    def getCipher(self):
        return self.__cipher

    def getFilesID(self):
        return self.__files_id

    def getDirsID(self):
        return self.__dirs_id

    def setSeed(self, seed: str):
        self.__seed = seed

    def setKey(self, key: str):
        self.__key = key

    def setType(self, backup_type: str):
        self.__type = backup_type

    def setAddress(self, address: str):
        self.__address = address

    def setFilesID(self, files_id: str):
        self.__files_id = files_id

    def setDirsID(self, dirs_id: str):
        self.__dirs_id = dirs_id