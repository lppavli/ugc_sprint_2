from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_host: str = 'localhost'
    kafka_port: int = 9092
    jwt_secret_key: str = 'top_secret'
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
    MONGO_DB = "ugc_db"
    MONGO_COLLECTION_LIKE = "likedFilms"
    DEFAULT_LIMIT = 10
    DEFAULT_OFFSET = 0

    class Config:
        env_file = ".env"

settings = Settings()