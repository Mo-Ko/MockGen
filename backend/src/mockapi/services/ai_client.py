import openai
import google.generativeai as genai
import json
from pathlib import Path
from mockapi.utils.logger import get_logger
from mockapi.core.config import app_settings


class AIClient:
    def __init__(self, openai_key: str | None, gemini_key: str | None) -> None:
        self.logger = get_logger("ai_service")
        self.openai_client = None
        if openai_key:
            self.openai_client = openai.AsyncOpenAI(api_key=openai_key)
            self.logger.info("OpenAI client configured.")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.logger.info("Gemini client configured.")

    def _build_prompt(self, prompt: str, api_type: str) -> str:
        try:
            prompt_template_path = app_settings.PROMPTS_DIR / f"{api_type}_api.prompt"
            return prompt_template_path.read_text(encoding="utf-8").format(prompt=prompt)
        except Exception as e:
            self.logger.error(f"Error building prompt for {api_type}: {e}")
            raise RuntimeError(f"Prompt template for {api_type} is invalid.")

    async def generate_schema(self, prompt: str, api_type: str, llm: str) -> object:
        instructions = self._build_prompt(prompt, api_type)
        self.logger.info(f"Generating schema with {llm.upper()}...")
        
        content = ""
        try:
            if llm == "openai":
                if not self.openai_client: raise RuntimeError("OpenAI client not configured.")
                response = await self.openai_client.chat.completions.create(
                    model=app_settings.OPENAI_MODEL,
                    messages=[{"role": "user", "content": instructions}],
                    temperature=0.0,
                    response_format={"type": "json_object"}
                )
                content = response.choices[0].message.content
            else: # gemini
                model = genai.GenerativeModel(app_settings.GEMINI_MODEL)
                response = await model.generate_content_async(
                    instructions,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.0,
                        response_mime_type="application/json"
                    )
                )
                content = response.text
        except Exception as e:
            self.logger.error(f"Error during AI API call to {llm.upper()}: {e}")
            raise RuntimeError("AI service communication failed.")

        try:
            self.logger.info(f"Raw JSON response from AI: {content}")
            data = json.loads(content)
            
            # THE FIX: Handle potential nesting from Gemini
            if "response" in data and isinstance(data["response"], dict):
                self.logger.info("Found nested 'response' key, using its content.")
                data = data["response"]

            if api_type == "rest":
                if not all(k in data for k in ["title", "paths", "components"]):
                    raise KeyError("Required keys (title, paths, components) not in AI response.")
                return {
                    "openapi": "3.0.0",
                    "info": {"title": data["title"], "version": "1.0.0"},
                    "paths": data["paths"],
                    "components": data["components"],
                }
            
            # For GraphQL
            if "sdl" not in data:
                raise KeyError("Required key 'sdl' not in AI response.")
            return data["sdl"].strip()

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            self.logger.error(f"Failed to parse or interpret AI JSON response: {e}\nRaw: {content}")
            raise RuntimeError("AI returned a malformed or unexpected JSON structure.")