"""
Enterprise Configuration Management
Centralizes all settings, model configs, and environment variables.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal
import os
from dotenv import load_dotenv

# Load .env immediately so all downstream imports see the variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings with validation and defaults."""

    # ── LLM Configuration ─────────────────────────────────────────────────────
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    model_name: str = Field(default="gpt-4o-mini", env="MODEL_NAME")
    temperature: float = Field(default=0.3, ge=0.0, le=2.0, env="TEMPERATURE")
    max_tokens: int = Field(default=4000, ge=100, le=16000, env="MAX_TOKENS")

    # ── Agent Behavior ─────────────────────────────────────────────────────────
    agent_verbose: bool = Field(default=False, env="AGENT_VERBOSE")
    max_iterations: int = Field(default=10, ge=1, le=50, env="MAX_ITERATIONS")
    enable_memory: bool = Field(default=True, env="ENABLE_MEMORY")
    max_search_results: int = Field(default=6, ge=1, le=20, env="MAX_SEARCH_RESULTS")

    # ── Application ────────────────────────────────────────────────────────────
    app_title: str = "NEXUS · Multi-Agent Intelligence Platform"
    app_version: str = "2.0.0"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO", env="LOG_LEVEL"
    )

    # ── Output ─────────────────────────────────────────────────────────────────
    output_dir: str = Field(default="outputs", env="OUTPUT_DIR")
    max_history_items: int = Field(default=20, env="MAX_HISTORY_ITEMS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Singleton instance
settings = Settings()

# Ensure output directory exists
os.makedirs(settings.output_dir, exist_ok=True)
