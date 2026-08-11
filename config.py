from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.providers.groq import GroqProvider
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.fallback import FallbackModel
from pydantic import Field

class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', env_file_encoding='utf-8')
    db_user: str = Field()
    db_host: str = Field()
    db_password: str = Field()
    db_name: str = Field()
    seed_db: bool = Field()

class AgentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', env_file_encoding='utf-8')
    google_api_key: str = Field()
    google_api_model: str = Field()
    groq_api_model: str = Field()
    groq_api_key: str = Field()

    def get_combo_model(self):
        groq_provider = GroqProvider(api_key=self.groq_api_key)
        groq_model = GroqModel(self.groq_api_model, provider=groq_provider)
        provider = GoogleProvider(api_key=self.google_api_key)
        google_model = GoogleModel(self.google_api_model, provider=provider)

        return FallbackModel(
            google_model
            ,groq_model
        )
