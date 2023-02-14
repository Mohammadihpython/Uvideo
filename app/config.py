from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_PASSWORD: str
    MONGO_INITDB_USERNAME: str
    MONGO_HOST :str
    MONGO_PORT:str
    ALGORITHMHASH:str
    SECRET:str
    # JWT_PUBLIC_KEY: str
    # JWT_PRIVATE_KEY: str
    # REFRESH_TOKEN_EXPIRES_IN: int
    # ACCESS_TOKEN_EXPIRES_IN: int
    # JWT_ALGORITHM: str

    # CLIENT_ORIGIN: str

    class Config:
        env_file = '../.env'


settings = Settings()
