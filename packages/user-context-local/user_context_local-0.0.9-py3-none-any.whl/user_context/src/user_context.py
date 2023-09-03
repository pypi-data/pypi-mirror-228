import sys
import os
from our_url.src.index import UrlCirclez
import json
from typing import Any
import jwt
from our_url.src.action_name_enum import ActionName
from our_url.src.entity_name_enum import EntityName
from our_url.src.component_name_enum import ComponentName
from language_local_python_package.src.language_enum_class import LanguageCode
from dotenv import load_dotenv
import requests
load_dotenv()
ENVIORNMENT_NAME = os.getenv('ENVIRONMENT_NAME')
VERSION = 1
BRAND_NAME = os.getenv('BRAND_NAME')

class UserContext:
    _instance = None
    def __new__(cls, email: str = None, password: str = None):
        if cls._instance is None:
            cls._instance = super(UserContext, cls).__new__(cls)
            cls._instance._initialize(email, password)
        return cls._instance
    def _initialize(self, email: str, password: str):
        self.user_id = None
        self.profile_id = None
        self.language = None
        jwt_token = self.authenticate(email, password)
        self.extractIdFromJwt(jwt_token)
        
    @staticmethod
    def getUser(email: str = None, password: str = None):
        logger.start(object={"email": email, "passowrd": password})
        if UserContext._instance is None:
            if email is None or password is None or email=="" or password=="":
                raise Exception("please insert in your .env PRODUCT_USERNAME and PRODUCT_PASSWORD")
            UserContext._instance = UserContext(email=email, password=password)
        logger.end(object={"user": str(UserContext._instance)})
        return UserContext._instance
    
    
    def set_user_id(self, user_id: int) -> None:
        logger.start(object={"user_id": user_id})
        self.user_id = user_id
        logger.end()

    def set_profile_id(self, profile_id: int) -> None:
        logger.start(object={"profile_id": profile_id})
        self.profile_id = profile_id
        logger.end()

    def get_user_id(self) -> int:
        logger.start()
        logger.end(object={"user_id": self.user_id})
        return self.user_id

    def get_profile_id(self) -> int:
        logger.start()
        logger.end(object={"user_id": self.profile_id})
        return self.profile_id

    def get_language(self) -> str:
        logger.start()
        logger.end(object={"language": self.language})
        return self.language

    def set_language(self, language: LanguageCode) -> None:
        logger.start(object={"language": language.value})
        self.language = language.value
        logger.end()

    def extractIdFromJwt(self, jwt_token: str) -> None:
        if jwt_token is None or jwt_token=="":
            raise Exception("Your .env PRODUCT_NAME or PRODUCT_PASSWORD is wrong")
        logger.start(object={"jwt_token": jwt_token})
        try:
            secret_key = os.getenv("JWT_SECRET_KEY")
            if secret_key is not None:
                decoded_payload = jwt.decode(jwt_token, secret_key, algorithms=["HS256"],options={"verify_signature": False})
                self.profile_id = int(decoded_payload.get('profileId'))
                self.user_id = int(decoded_payload.get('userId'))
                self.language = decoded_payload.get('language')
                logger.end()
        except jwt.ExpiredSignatureError as e:
            # Handle token expiration
            logger.exception(object=e)
            print("Error:JWT token has expired.", sys.stderr)
            logger.end()
            raise
        except jwt.InvalidTokenError as e:
            # Handle invalid token
            logger.exception(object=e)
            print("Error:Invalid JWT token.", sys.stderr)
            logger.end()
            raise

    def authenticate(self, email: str, password: str):
        logger.start(object={"email":email,"password":password})
        try:
            url_circlez = UrlCirclez()
            url_jwt = url_circlez.endpoint_url(
                brand_name=BRAND_NAME,
                env_name=ENVIORNMENT_NAME,
                component=ComponentName.AUTHENTICATION.value,
                entity=EntityName.AUTH_LOGIN.value,
                version=VERSION,
                action=ActionName.LOGIN.value
            )
            data = {"email": email, "password": password}
            headers = {"Content-Type": "application/json"}
            output = requests.post(
                url=url_jwt, data=json.dumps(data, separators=(",", ":")), headers=headers
            )
            jwt_token = output.json()["data"]["token"]
            logger.end(object={"jwt_token":jwt_token})
            return jwt_token
        except Exception as e:
            logger.exception(object=e)
            logger.end()
            
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
USER_CONTEXT_LOCAL_PYTHON_COMPONENT_ID = 197
USER_CONTEXT_LOCAL_PYTHON_COMPONENT_NAME = "User Context python package"
DEVELOPER_EMAIL = "idan.a@circ.zone"
obj = {
    'component_id': USER_CONTEXT_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': USER_CONTEXT_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=obj)
