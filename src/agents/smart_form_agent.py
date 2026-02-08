"""
Smart form agent using Selenium (works with Streamlit on Windows).
No async/event loop conflicts!
"""
from typing import Dict, Any, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re
import time

from src.utils.logging_config import logger


class SmartFormAgent:
    """
    Agent that discovers form fields using Selenium (Streamlit-compatible).
    """
    
    def __init__(self):
        self.driver = None
        self.discovered_fields: List[Dict[str, str]] = []
        self.collected_data: Dict[str, Any] = {}
        
    def start_browser(self):
        """Launch Chrome using Selenium."""
        if not self.driver:
            options = Options()
            # options.add_argument('--headless')  # Uncomment for headless mode
            options.add_argument('--start-maximized')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            self.driver = webdriver.Chrome(options=options)
            logger.info("selenium_browser_started")
    
    def search_and_navigate(self, service_type: str) -> str:
        """Navigate to service page using Selenium."""
        self.start_browser()
        
        # Direct URLs for different services
        direct_urls = {
            "mppsc": "https://www.mponline.gov.in/Portal/Examinations/MPPSC/",
            "electricity": "https://www.mponline.gov.in/Portal/Services/MPEDC/Home.aspx",
            "university": "https://www.mponline.gov.in/Portal/Services/Universities/Home.aspx"
        }
        
        logger.info("selenium_navigating", service=service_type)
        
        try:
            target_url = direct_urls.get(service_type, "https://www.mponline.gov.in")
            self.driver.get(target_url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            time.sleep(2)  # Wait for dynamic content
            
            current_url = self.driver.current_url
            logger.info("selenium_navigated", url=current_url)
            return f"✅ Successfully navigated to the form page!\nURL: {current_url}"
        except Exception as e:
            logger.error("selenium_navigation_failed", error=str(e))
            return f"❌ Navigation failed: {str(e)}"
    
    def discover_form_fields(self) -> List[Dict[str, str]]:
        """Discover form fields using Selenium."""
        if not self.driver:
            return []
        
        logger.info("selenium_discovering_fields")
        
        try:
            # Find all input, select, and textarea elements
            inputs = self.driver.find_elements(By.CSS_SELECTOR, "input, select, textarea")
            
            discovered = []
            seen_names = set()
            
            for elem in inputs:
                try:
                    name = elem.get_attribute("name") or elem.get_attribute("id") or ""
                    if not name or name in seen_names:
                        continue
                    
                    input_type = elem.get_attribute("type") or "text"
                    
                    # Skip hidden and submit buttons
                    if input_type in ["hidden", "submit", "button"]:
                        continue
                    
                    # Skip if already has value
                    value = elem.get_attribute("value") or ""
                    if value:
                        continue
                    
                    # Find label
                    label = ""
                    try:
                        # Try to find associated label
                        elem_id = elem.get_attribute("id")
                        if elem_id:
                            label_elem = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{elem_id}']")
                            label = label_elem.text.strip()
                    except:
                        pass
                    
                    if not label:
                        label = elem.get_attribute("placeholder") or name or "Unknown Field"
                    
                    # Check if required
                    required = elem.get_attribute("required") is not None
                    
                    discovered.append({
                        'name': name,
                        'label': label,
                        'type': input_type,
                        'required': required
                    })
                    seen_names.add(name)
                    
                except Exception as e:
                    continue
            
            self.discovered_fields = discovered
            logger.info("selenium_fields_discovered", count=len(discovered))
            
            return discovered
            
        except Exception as e:
            logger.error("selenium_field_discovery_failed", error=str(e))
            return []
    
    def get_next_question(self) -> Optional[str]:
        """Get the next question to ask user."""
        for field in self.discovered_fields:
            field_name = field['name']
            
            if field_name not in self.collected_data:
                label = field['label']
                field_type = field['type']
                required = "required" if field['required'] else "optional"
                
                # Generate human-friendly question
                if field_type == 'email':
                    return f"📧 What is your {label.lower()}?"
                elif field_type == 'tel' or 'mobile' in label.lower() or 'phone' in label.lower():
                    return f"📱 What is your {label.lower()}?"
                elif field_type == 'date' or 'birth' in label.lower():
                    return f"📅 What is your {label.lower()}? (DD/MM/YYYY)"
                elif field_type == 'select':
                    return f"📋 Please select your {label.lower()}"
                else:
                    return f"✏️  What is your {label.lower()}? ({required})"
        
        return None
    
    def extract_data(self, message: str) -> Dict[str, Any]:
        """Extract data from user message."""
        data = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, message)
        if emails:
            data["email"] = emails[0]
        
        # Mobile
        mobile_pattern = r'\b[6-9]\d{9}\b'
        mobiles = re.findall(mobile_pattern, message)
        if mobiles:
            data["mobile"] = mobiles[0]
        
        # Generic text for current missing field
        next_field = self.get_current_missing_field()
        if next_field and not data:
            clean_message = message.strip()
            data[next_field] = clean_message
        
        return data
    
    def get_current_missing_field(self) -> Optional[str]:
        """Get the name of the current field we're asking about."""
        for field in self.discovered_fields:
            if field['name'] not in self.collected_data:
                return field['name']
        return None
    
    def fill_form_incrementally(self):
        """Fill form with collected data using Selenium."""
        if not self.driver:
            return
        
        try:
            for field_name, value in self.collected_data.items():
                field = next((f for f in self.discovered_fields if f['name'] == field_name), None)
                if field:
                    try:
                        # Find element by name
                        elem = self.driver.find_element(By.NAME, field_name)
                        
                        if field['type'] == 'select':
                            from selenium.webdriver.support.ui import Select
                            select = Select(elem)
                            select.select_by_visible_text(str(value))
                        else:
                            elem.clear()
                            elem.send_keys(str(value))
                        
                        logger.info("selenium_field_filled", field=field_name)
                        time.sleep(0.3)  # Visual feedback
                    except Exception as e:
                        logger.warning("selenium_fill_field_failed", field=field_name, error=str(e))
            
            # Take screenshot
            self.driver.save_screenshot('data/screenshots/selenium_filled.png')
            
        except Exception as e:
            logger.error("selenium_fill_failed", error=str(e))
    
    def cleanup(self):
        """Close browser."""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def get_progress(self) -> str:
        """Get progress string."""
        total = len(self.discovered_fields)
        filled = len(self.collected_data)
        if total == 0:
            return ""
        return f"({filled}/{total} fields filled)"
