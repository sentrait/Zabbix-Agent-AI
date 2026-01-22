import json
import os
from typing import Dict, Any

CONFIG_FILE = "ai_agent_config.json"

class ConfigService:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), CONFIG_FILE)
        self._ensure_config_exists()

    def _ensure_config_exists(self):
        if not os.path.exists(self.config_path):
            default_config = {
                "provider": "bedrock",
                "aws_region": os.getenv("AWS_REGION", "us-east-1"),
                "aws_access_key": os.getenv("AWS_ACCESS_KEY_ID", ""),
                "aws_secret_key": os.getenv("AWS_SECRET_ACCESS_KEY", ""),
                "bedrock_model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                "openai_api_key": "",
                "openai_model": "gpt-4o",
                "gemini_api_key": "",
                "gemini_model": "gemini-1.5-pro-latest"
            }
            self.save_config(default_config)

    def get_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}

    def save_config(self, config: Dict[str, Any]):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
            raise e

config_service = ConfigService()
