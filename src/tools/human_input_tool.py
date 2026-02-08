"""Human-in-the-loop input tool for CAPTCHA and payment confirmation."""
import asyncio
from typing import Optional, Any
from src.utils.logging_config import logger


class HumanInputTool:
    """
    Manages human-in-the-loop interactions via Streamlit.
    """
    
    def __init__(self):
        """Initialize human input tool."""
        self.pending_requests = {}
        self.responses = {}
    
    async def request_input(
        self,
        request_id: str,
        prompt: str,
        input_type: str = "text",
        timeout: int = 300
    ) -> Optional[Any]:
        """
        Request input from human user.
        
        Args:
            request_id: Unique identifier for this request
            prompt: Prompt to display to user
            input_type: Type of input ('text', 'confirmation', 'file')
            timeout: Timeout in seconds
            
        Returns:
            User's response or None if timeout
        """
        logger.info(
            "human_input_requested",
            request_id=request_id,
            prompt=prompt,
            type=input_type
        )
        
        # Store pending request
        self.pending_requests[request_id] = {
            "prompt": prompt,
            "type": input_type,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Wait for response with timeout
        start_time = asyncio.get_event_loop().time()
        while True:
            # Check if response received
            if request_id in self.responses:
                response = self.responses.pop(request_id)
                self.pending_requests.pop(request_id, None)
                
                logger.info(
                    "human_input_received",
                    request_id=request_id,
                    response_length=len(str(response))
                )
                
                return response
            
            # Check timeout
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed > timeout:
                self.pending_requests.pop(request_id, None)
                logger.warning("human_input_timeout", request_id=request_id)
                return None
            
            # Sleep briefly before checking again
            await asyncio.sleep(0.5)
    
    def submit_response(self, request_id: str, response: Any):
        """
        Submit response for a pending request.
        
        Args:
            request_id: Request identifier
            response: User's response
        """
        self.responses[request_id] = response
        logger.info("human_response_submitted", request_id=request_id)
    
    def get_pending_request(self, request_id: str) -> Optional[dict]:
        """
        Get details of a pending request.
        
        Args:
            request_id: Request identifier
            
        Returns:
            Request details or None
        """
        return self.pending_requests.get(request_id)
    
    def list_pending_requests(self) -> list[str]:
        """
        List all pending request IDs.
        
        Returns:
            List of request IDs
        """
        return list(self.pending_requests.keys())
    
    def cancel_request(self, request_id: str):
        """
        Cancel a pending request.
        
        Args:
            request_id: Request identifier
        """
        self.pending_requests.pop(request_id, None)
        self.responses.pop(request_id, None)
        logger.info("human_request_cancelled", request_id=request_id)


# Global human input tool instance
human_input_tool = HumanInputTool()
