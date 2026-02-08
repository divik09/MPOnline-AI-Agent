"""Conversational chat agent for understanding user requests."""
from typing import Dict, Any, List, Optional
import re

from src.utils.browser_use_helper import get_configured_llm
from src.utils.logging_config import logger

from dataclasses import dataclass, field


@dataclass
class UserIntent:
    """Structured user intent extracted from conversation."""
    service_type: Optional[str] = None
    action: str = "get_info"
    extracted_data: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.8
    needs_clarification: bool = True
    clarifying_question: Optional[str] = None


class ConversationalAgent:
    """
    Chat-based agent that understands natural language and triggers automation.
    
    Example conversations:
    - "I want to apply for MPPSC" -> Understands intent, asks for details
    - "Search for electricity bill payment" -> Searches and navigates
    - "My name is John and email is john@example.com" -> Extracts data
    """
    
    def __init__(self):
        self.llm = None  # Only created when needed
        self.conversation_history: List[Dict[str, str]] = []
        self.collected_data: Dict[str, Any] = {}
        self.current_service: Optional[str] = None
    
    def understand_intent(self, user_message: str) -> UserIntent:
        """
        Understand user intent from natural language using pattern matching.
        
        Args:
            user_message: What the user said
            
        Returns:
            Structured intent with extracted information
        """
        logger.info("understanding_intent", message=user_message[:100])
        
        try:
            # Simple pattern-based understanding
            intent = UserIntent(
                service_type=self._extract_service_type("", user_message),
                action=self._extract_action("", user_message),
                extracted_data=self._extract_data(user_message),
                confidence=0.8,
                needs_clarification=self._needs_clarification(user_message),
                clarifying_question=self._generate_question(user_message)
            )
            
            logger.info("intent_understood", service=intent.service_type, action=intent.action)
            return intent
            
        except Exception as e:
            logger.error("intent_understanding_failed", error=str(e))
            return UserIntent(
                action="get_info",
                confidence=0.3,
                needs_clarification=True,
                clarifying_question="I'm not sure I understood. Could you tell me what service you need help with?"
            )
    
    def _extract_service_type(self, content: str, original: str) -> Optional[str]:
        """Extract service type from message."""
        text = (content + " " + original).lower()
        
        if any(word in text for word in ["mppsc", "psc", "recruitment", "government job"]):
            return "mppsc"
        elif any(word in text for word in ["electricity", "bijli", "bill", "power"]):
            return "electricity"
        elif any(word in text for word in ["university", "college", "admission", "barkatullah", "jiwaji"]):
            return "university"
        
        return None
    
    def _extract_action(self, content: str, original: str) -> str:
        """Extract user action."""
        text = (content + " " + original).lower()
        
        if any(word in text for word in ["apply", "application", "fill form", "register"]):
            return "apply"
        elif any(word in text for word in ["search", "find", "look for", "google"]):
            return "search"
        elif any(word in text for word in ["pay", "payment", "bill"]):
            return "pay_bill"
        elif any(word in text for word in ["status", "check", "track"]):
            return "check_status"
        else:
            return "get_info"
    
    def _extract_data(self, message: str) -> Dict[str, Any]:
        """Extract structured data from free-form text."""
        data = {}
        message_lower = message.lower()
        
        # Name extraction patterns
        if "name is" in message_lower or "my name" in message_lower:
            # Simple extraction - can be enhanced with NER
            words = message.split()
            for i, word in enumerate(words):
                if word.lower() in ["is", "name"]:
                    if i + 1 < len(words):
                        # Get next 2-3 words as name
                        name_parts = words[i+1:min(i+4, len(words))]
                        data["full_name"] = " ".join(name_parts).strip(".,")
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, message)
        if emails:
            data["email"] = emails[0]
        
        # Mobile extraction
        mobile_pattern = r'\b[6-9]\d{9}\b'
        mobiles = re.findall(mobile_pattern, message)
        if mobiles:
            data["mobile"] = mobiles[0]
        
        return data
    
    def _needs_clarification(self, message: str) -> bool:
        """Check if we need more information."""
        # If message is very short or vague
        if len(message.split()) < 3:
            return True
        
        # If we don't know the service type yet
        if not self.current_service:
            text = message.lower()
            has_service = any(word in text for word in [
                "mppsc", "electricity", "university", "bill", "application"
            ])
            return not has_service
        
        return False
    
    def _generate_question(self, message: str) -> Optional[str]:
        """Generate a clarifying question based on what's missing."""
        # First, check if we know the service
        if not self.current_service:
            return "What would you like help with today? I can help with:\n• **MPPSC Applications** (government jobs)\n• **Electricity Bill Payments**\n• **University Admissions**\n\nJust tell me what you need!"
        
        # Define required fields for each service in order
        required_fields_order = {
            "mppsc": [
                ("full_name", "What is your full name?"),
                ("father_name", "What is your father's name?"),
                ("mother_name", "What is your mother's name?"),
                ("date_of_birth", "What is your date of birth? (DD/MM/YYYY)"),
                ("gender", "What is your gender? (Male/Female/Other)"),
                ("category", "What is your category? (General/OBC/SC/ST)"),
                ("email", "What is your email address?"),
                ("mobile", "What is your mobile number?"),
                ("address", "What is your full address?"),
                ("district", "Which district are you from?"),
                ("state", "Which state? (Usually Madhya Pradesh)"),
                ("pincode", "What is your pincode?"),
                ("qualification", "What is your highest qualification?")
            ],
            "electricity": [
                ("consumer_number", "What is your electricity consumer number?"),
                ("email", "What is your email address for the receipt?"),
                ("mobile", "What is your mobile number?")
            ],
            "university": [
                ("full_name", "What is your full name?"),
                ("father_name", "What is your father's name?"),
                ("date_of_birth", "What is your date of birth?"),
                ("email", "What is your email address?"),
                ("mobile", "What is your mobile number?"),
                ("course", "Which course are you applying for?")
            ]
        }
        
        if self.current_service in required_fields_order:
            # Go through fields in order and ask for first missing one
            for field, question in required_fields_order[self.current_service]:
                if field not in self.collected_data:
                    # Show progress
                    total = len(required_fields_order[self.current_service])
                    filled = len(self.collected_data)
                    progress = f"({filled}/{total} details collected)\n\n"
                    return progress + question
            
            # All fields collected!
            return None
        
        return "Could you provide more details about your application?"
    
    def chat(self, user_message: str) -> Dict[str, Any]:
        """
        Process user message and return response.
        
        Args:
            user_message: What user said
            
        Returns:
            Response with action to take
        """
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Understand intent
        intent = self.understand_intent(user_message)
        
        # Update service if detected
        if intent.service_type:
            self.current_service = intent.service_type
        
        # Collect extracted data
        self.collected_data.update(intent.extracted_data)
        
        # Generate response
        response = {
            "message": "",
            "action": None,
            "data": self.collected_data.copy(),
            "service": self.current_service,
            "ready_to_automate": False
        }
        
        if intent.needs_clarification and intent.clarifying_question:
            response["message"] = intent.clarifying_question
        elif intent.action == "search":
            response["message"] = f"I'll help you search for {self.current_service or 'what you need'}. Let me gather some details first."
            if self.current_service:
                response["action"] = "initiate_search"
        elif intent.action == "apply":
            if self._has_minimum_data():
                response["message"] = "Great! I have enough information to start the application. Should I proceed with the automation?"
                response["ready_to_automate"] = True
                response["action"] = "ready_to_automate"
            else:
                response["message"] = "I'll help you with the application. " + (intent.clarifying_question or "")
        else:
            response["message"] = f"I understand you want to {intent.action} for {self.current_service or 'a service'}. How can I help?"
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response["message"]
        })
        
        return response
    
    def _has_minimum_data(self) -> bool:
        """Check if we have minimum data to start automation."""
        if not self.current_service:
            return False
        
        if self.current_service == "mppsc":
            required = ["full_name", "email", "mobile"]
            return all(field in self.collected_data for field in required)
        elif self.current_service == "electricity":
            return "consumer_number" in self.collected_data
        
        return False
    
    def get_automation_task(self) -> str:
        """Generate automation task from conversation."""
        if not self.current_service:
            return ""
        
        if self.current_service == "mppsc":
            return f"""
            Search Google for "MPOnline MPPSC application", navigate to the form,
            and fill it with the collected data: {self.collected_data}
            """
        elif self.current_service == "electricity":
            return f"""
            Search Google for "MPOnline electricity bill payment",
            enter consumer number {self.collected_data.get('consumer_number')}
            and proceed to payment
            """
        
        return f"Search Google for MPOnline {self.current_service}"
