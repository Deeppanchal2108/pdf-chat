from uuid import UUID
from dotenv import load_dotenv
import os

load_dotenv()


def store_meta(user_id : UUID, file_name:str ,  content_type :str, file_size:float ):


