from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
	app_name: str = Field("StudyGenie API", env="APP_NAME")
	app_version: str = Field("0.1.0", env="APP_VERSION")
	openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")
	embedding_model: str = Field("text-embedding-3-small", env="EMBEDDING_MODEL")
	llm_model: str = Field("gpt-4o-mini", env="LLM_MODEL")
	faiss_dir: str = Field("/workspace/data/faiss", env="FAISS_DIR")
	ocr_provider: str = Field("tesseract", env="OCR_PROVIDER")
	# database
	database_url: str = Field("sqlite+aiosqlite:///workspace/data/studygenie.db", env="DATABASE_URL")

	class Config:
		env_file = ".env"
		case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
	return Settings()