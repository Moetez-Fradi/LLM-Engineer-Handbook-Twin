from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TEXT_EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    RERANKING_CROSS_ENCODER_MODEL_ID: str = "cross-encoder/ms-marcoMiniLM-L-4-v2"

    RAG_MODEL_DEVICE: str = "cpu"

    USE_QDRANT_CLOUD: bool = False
    QDRANT_DATABASE_HOST: str = "localhost"
    QDRANT_DATABASE_PORT: int = 6333

    DATABASE_HOST: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "extracted"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
