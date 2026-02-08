"""Electricity bill payment service template."""
from typing import Dict, Any


class ElectricityTemplate:
    """Template for electricity bill payment."""
    
    @staticmethod
    def get_url() -> str:
        """Get electricity bill payment URL."""
        return "https://www.mponline.gov.in/Portal/Services/Electricity/BillPayment.aspx"
    
    @staticmethod
    def get_login_selectors() -> Dict[str, str]:
        """Login not required for bill payment."""
        return {}
    
    @staticmethod
    def get_field_mappings(step: str) -> Dict[str, Dict[str, Any]]:
        """Get field mappings for electricity bill payment."""
        if step == "form_fill":
            return {
                "consumer_number": {
                    "selector": "#txtConsumerNo",
                    "type": "text",
                    "required": True,
                    "description": "Electricity consumer number"
                },
                "mobile": {
                    "selector": "#txtMobile",
                    "type": "text",
                    "required": True,
                    "description": "Registered mobile number"
                },
                "email": {
                    "selector": "#txtEmail",
                    "type": "text",
                    "required": False,
                    "description": "Email for receipt"
                }
            }
        
        return {}
    
    @staticmethod
    def get_validation_rules() -> Dict[str, Any]:
        """Get validation rules."""
        return {
            "consumer_number_length": 10
        }
    
    @staticmethod
    def get_service_info() -> Dict[str, str]:
        """Get service information."""
        return {
            "name": "Electricity Bill Payment",
            "full_name": "MP Electricity Bill Payment",
            "description": "Pay your electricity bill online",
            "category": "Bill Payments"
        }


class UniversityTemplate:
    """Generic template for university applications."""
    
    @staticmethod
    def get_url() -> str:
        """Get university URL (can be customized per university)."""
        return "https://bubhopal.mponline.gov.in/Portal/index.aspx"
    
    @staticmethod
    def get_login_selectors() -> Dict[str, str]:
        """Get login selectors for university portal."""
        return {
            "username": "#txtUsername",
            "password": "#txtPassword",
            "submit": "#btnLogin",
            "logged_in_indicator": ".student-dashboard"
        }
    
    @staticmethod
    def get_field_mappings(step: str) -> Dict[str, Dict[str, Any]]:
        """Get field mappings for university application."""
        if step == "form_fill":
            return {
                "student_name": {
                    "selector": "#txtStudentName",
                    "type": "text",
                    "required": True,
                    "description": "Student's full name"
                },
                "father_name": {
                    "selector": "#txtFatherName",
                    "type": "text",
                    "required": True,
                    "description": "Father's name"
                },
                "date_of_birth": {
                    "selector": "#txtDOB",
                    "type": "text",
                    "required": True,
                    "description": "Date of birth"
                },
                "email": {
                    "selector": "#txtEmail",
                    "type": "text",
                    "required": True,
                    "description": "Email address"
                },
                "mobile": {
                    "selector": "#txtMobile",
                    "type": "text",
                    "required": True,
                    "description": "Mobile number"
                },
                "course": {
                    "selector": "#ddlCourse",
                    "type": "select",
                    "required": True,
                    "description": "Course selection"
                }
            }
        
        elif step == "document_upload":
            return {
                "photo": {
                    "selector": "#filePhoto",
                    "type": "file",
                    "required": True,
                    "description": "Passport photo"
                },
                "marksheet": {
                    "selector": "#fileMarksheet",
                    "type": "file",
                    "required": True,
                    "description": "Previous marksheet"
                }
            }
        
        return {}
    
    @staticmethod
    def get_validation_rules() -> Dict[str, Any]:
        """Get validation rules."""
        return {
            "photo_max_size": 102400,
            "marksheet_max_size": 512000
        }
    
    @staticmethod
    def get_service_info() -> Dict[str, str]:
        """Get service information."""
        return {
            "name": "University Application",
            "full_name": "University Admission Application",
            "description": "Apply for university admissions",
            "category": "University"
        }
