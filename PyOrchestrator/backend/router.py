import litellm
import os
from typing import Dict, Any, Optional

class ModelRouter:
    """
    Routes LLM requests to the appropriate provider/server based on model name.
    """
    
    def __init__(self):
        # Configuration for local servers
        self.devstral_url = os.getenv("DEVSTRAL_URL", "http://192.168.4.119:1234/v1")
        self.local_llm_url = os.getenv("LOCAL_LLM_URL", "http://localhost:1234/v1")
        
    async def chat_completion(self, model: str, messages: list, temperature: float = 0.7) -> str:
        """
        Routes the chat completion request.
        """
        try:
            params = {
                "model": model,
                "messages": messages,
                "temperature": temperature
            }

            # Custom Routing Logic
            if model == "devstral-3090":
                # Route to 3090 Linux Server
                params["model"] = "openai/devstral-3090" # LiteLLM convention for generic OpenAI-compatible
                params["api_base"] = self.devstral_url
                params["api_key"] = "sk-placeholder" # Local often ignores this
                
            elif model == "m4-max":
                 # Route to Mac Local Server
                # Map 'm4-max' alias to the actual loaded model
                # Prefix with openai/ so LiteLLM treats it as an OpenAI-compatible endpoint (local)
                # instead of trying to hit the Mistral API directly.
                params["model"] = "openai/mistralai/devstral-small-2-2512"
                params["api_base"] = self.local_llm_url
                params["api_key"] = "lm-studio"
            
            else:
                # Default fallback for "gpt-4" or others -> Route to Local LLM (LM Studio)
                # LiteLLM requires 'openai/' prefix for generic compatible servers
                params["model"] = f"openai/{model}"
                params["api_base"] = self.local_llm_url
                # LiteLLM throws error if api_key is missing, even for local
                params["api_key"] = "lm-studio"

            # Execute Call
            response = await litellm.acompletion(**params)
            
            return response.choices[0].message.content

        except Exception as e:
            # Simple retry logic could go here
            print(f"Error in chat_completion: {e}")
            raise e
