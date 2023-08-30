from transwarp_embedding_hub.base_embedding import *
import os
import yaml
import openai


class Azure(BaseEmbedding):
    """openai embedding strategy."""

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(dir_path, 'config.yaml')
        with open(config_path) as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)['model']['azure']
        self.openai_api_key = self.config['apikey']
        self.embedding_engine = self.config['engine']
        self.openai_api_version = self.config['version']
        self.openai_api_url = self.config['url']

    # 检查模型是否可用
    def check_model_active(self, api_key: str = None, embedding_engine: str = None):
        try:
            self.embed_string("你好", api_key, embedding_engine)
            return True  # 如果没有发生异常，说明模型可用
        except Exception as e:
            print(f"Model not available. Error: {e}")
            return False  # 如果发生了异常，说明模型不可用

    # 将字符串转为向量
    def embed_string(self, text: str, api_key: str = None, embedding_engine: str = None, api_base: str = None,
                     api_version: str = None):

        if api_key is None:
            api_key = self.openai_api_key
        else:
            api_key = api_key

        if embedding_engine is None:
            embedding_engine = self.embedding_engine
        else:
            embedding_engine = embedding_engine

        if api_base is None:
            api_base = self.openai_api_url
        else:
            api_base = api_base

        if api_version is None:
            api_version = self.openai_api_version
        else:
            api_version = api_version

        openai.api_type = "azure"
        openai.api_key = api_key
        openai.api_base = api_base
        openai.api_version = api_version
        return openai.Embedding.create(
            input=text,
            engine=embedding_engine)["data"][0]["embedding"]
