import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "local"
    database_url: str = ""
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_db: str = "chemical_inventory"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    azure_database_url: str = ""
    
    @property
    def get_database_url(self) -> str:
        if self.environment == "azure":
            return self.azure_database_url
        return self.database_url or f"postgresql://{self.postgres_user}:{self.postgres_password}@db:5432/{self.postgres_db}"
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()