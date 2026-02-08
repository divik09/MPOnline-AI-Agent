"""Vision tool for element identification using multimodal LLMs."""
import base64
from pathlib import Path
from typing import Optional
from src import config
from src.utils.logging_config import logger


class VisionTool:
    """
    Uses GPT-4o or Claude 3.5 Sonnet to identify page elements from screenshots.
    """
    
    def __init__(self):
        """Initialize vision tool with configured LLM."""
        self.llm_config = config.get_llm_config()
        self.cache = {}  # Cache results to avoid repeated API calls
        
        if self.llm_config["provider"] == "openai":
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model=self.llm_config["model"],
                api_key=self.llm_config["api_key"],
                temperature=self.llm_config["temperature"],
            )
        elif self.llm_config["provider"] == "anthropic":
            from langchain_anthropic import ChatAnthropic
            self.llm = ChatAnthropic(
                model=self.llm_config["model"],
                api_key=self.llm_config["api_key"],
                temperature=self.llm_config["temperature"],
            )
        
        logger.info("vision_tool_initialized", provider=self.llm_config["provider"])
    
    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    async def identify_element(
        self,
        screenshot_path: str,
        field_name: str,
        field_description: Optional[str] = None
    ) -> dict:
        """
        Identify form element selector from screenshot.
        
        Args:
            screenshot_path: Path to screenshot image
            field_name: Name of the field to find (e.g., "email", "full_name")
            field_description: Optional description to help LLM
            
        Returns:
            Dictionary with selector and confidence score
        """
        # Check cache
        cache_key = f"{screenshot_path}:{field_name}"
        if cache_key in self.cache:
            logger.info("vision_tool_cache_hit", field=field_name)
            return self.cache[cache_key]
        
        try:
            # Encode image
            image_base64 = self._encode_image(screenshot_path)
            
            # Create prompt
            prompt = f"""You are a web automation expert. Analyze this screenshot of a form and identify the CSS selector or XPath for the following field:

Field Name: {field_name}
{f'Description: {field_description}' if field_description else ''}

Please provide:
1. The most reliable CSS selector or XPath for this field
2. A confidence score (0-100)
3. Any alternatives if the primary selector might fail

Respond in JSON format:
{{
    "selector": "css_selector_or_xpath",
    "type": "css|xpath",
    "confidence": 85,
    "alternatives": ["alternative1", "alternative2"],
    "notes": "any relevant observations"
}}"""

            # Call LLM with vision
            if self.llm_config["provider"] == "openai":
                from langchain_core.messages import HumanMessage
                
                message = HumanMessage(
                    content=[
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                )
                
                response = await self.llm.ainvoke([message])
                
            elif self.llm_config["provider"] == "anthropic":
                from langchain_core.messages import HumanMessage
                
                message = HumanMessage(
                    content=[
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_base64,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ]
                )
                
                response = await self.llm.ainvoke([message])
            
            # Parse response
            import json
            result = json.loads(response.content)
            
            # Cache result
            self.cache[cache_key] = result
            
            logger.info(
                "vision_tool_success",
                field=field_name,
                selector=result.get("selector"),
                confidence=result.get("confidence")
            )
            
            return result
            
        except Exception as e:
            logger.error("vision_tool_error", field=field_name, error=str(e))
            return {
                "selector": None,
                "type": "css",
                "confidence": 0,
                "alternatives": [],
                "notes": f"Error: {str(e)}"
            }
    
    def clear_cache(self):
        """Clear the selector cache."""
        self.cache.clear()
        logger.info("vision_tool_cache_cleared")


# Global vision tool instance
vision_tool = VisionTool()
