import os
from dotenv import load_dotenv

from common.path_utils import get_file_path


load_dotenv(get_file_path(".env"))


class Config:
    def __init__(self):
        # 大模型相关
        self.MODEL_API_KEY = os.getenv("MODEL_API_KEY")
        self.MODEL_BASE_URL = os.getenv("MODEL_BASE_URL")
        self.MODEL_NAME = os.getenv("MODEL_NAME")


if __name__ == "__main__":
    conf = Config()
    print(conf.MODEL_NAME)