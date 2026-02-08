"""MPPSC (Madhya Pradesh Public Service Commission) service template."""
from typing import Dict, Any


class MPPSCTemplate:
    """Template for MPPSC application forms."""
    
    @staticmethod
    def get_url() -> str:
        """Get MPPSC service URL."""
        return "https://www.mponline.gov.in/Portal/Examinations/MPPSC/Admin/Home.aspx"
    
    @staticmethod
    def get_login_selectors() -> Dict[str, str]:
        """
        Get login form selectors.
        
        Returns empty dict - MPPSC portal is publicly accessible, no login required.
        """
        return {}  # No login required for MPPSC public portal
    
    @staticmethod
    def get_field_mappings(step: str) -> Dict[str, Dict[str, Any]]:
        """
        Get field mappings for a specific step.
        
        Args:
            step: Current form step (e.g., 'form_fill', 'document_upload')
            
        Returns:
            Dictionary mapping field names to configurations
        """
        if step == "form_fill":
            return {
                "full_name": {
                    "selector": "#ctl00_ContentPlaceHolder1_txtName",
                    "type": "text",
                    "required": True,
                    "description": "Applicant's full name"
                },
                "father_name": {
                    "selector": "#ctl00_ContentPlaceHolder1_txtFatherName",
                    "type": "text",
                    "required": True,
                    "description": "Father's name"
                },
                "mother_name": {
                    "selector": "#ctl00_ContentPlaceHolder1_txtMotherName",
                    "type": "text",
                    "required": True,
                    "description": "Mother's name"
                },
                "date_of_birth": {
                    "selector": "#ctl00_ContentPlaceHolder1_txtDOB",
                    "type": "text",
                    "required": True,
                    "description": "Date of birth in DD/MM/YYYY format"
                },
                "gender": {
                    "selector": "#ctl00_ContentPlaceHolder1_ddlGender",
                    "type": "select",
                    "required": True,
                    "description": "Gender selection"
                },
                "category": {
                    "selector": "#ctl00_ContentPlaceHolder1_ddlCategory",
                    "type": "select",
                    "required": True,
                    "description": "Category (General/OBC/SC/ST)"
                },
                "email": {
                    "selector": "#ctl00_ContentPlaceHolder1_txtEmail",
                    "type": "text",
                    "required": True,
                    "description": "Email address"
                },
                "mobile": {
                    "selector": "#ctl00_ContentPlaceHolder1_txtMobile",
                    "type": "text",
                    "required": True,
                    "description": "Mobile number"
                },
                "address": {
                    "selector": "#ctl00_ContentPlaceHolder1_txtAddress",
                    "type": "text",
                    "required": True,
                    "description": "Permanent address"
                },
                "district": {
                    "selector": "#ctl00_ContentPlaceHolder1_ddlDistrict",
                    "type": "select",
                    "required": True,
                    "description": "District"
                },
                "state": {
                    "selector": "#ctl00_ContentPlaceHolder1_ddlState",
                    "type": "select",
                    "required": True,
                    "description": "State"
                },
                "pincode": {
                    "selector": "#ctl00_ContentPlaceHolder1_txtPincode",
                    "type": "text",
                    "required": True,
                    "description": "PIN code"
                },
                "qualification": {
                    "selector": "#ctl00_ContentPlaceHolder1_ddlQualification",
                    "type": "select",
                    "required": True,
                    "description": "Educational qualification"
                }
            }
        
        elif step == "document_upload":
            return {
                "photo": {
                    "selector": "#ctl00_ContentPlaceHolder1_filePhoto",
                    "type": "file",
                    "required": True,
                    "description": "Passport size photo (JPG, max 50KB)"
                },
                "signature": {
                    "selector": "#ctl00_ContentPlaceHolder1_fileSignature",
                    "type": "file",
                    "required": True,
                    "description": "Scanned signature (JPG, max 20KB)"
                },
                "certificate": {
                    "selector": "#ctl00_ContentPlaceHolder1_fileCertificate",
                    "type": "file",
                    "required": False,
                    "description": "Educational certificate (PDF, max 500KB)"
                }
            }
        
        return {}
    
    @staticmethod
    def get_validation_rules() -> Dict[str, Any]:
        """Get validation rules for the service."""
        return {
            "photo_max_size": 51200,  # 50KB
            "signature_max_size": 20480,  # 20KB
            "certificate_max_size": 512000,  # 500KB
            "photo_format": ["jpg", "jpeg"],
            "signature_format": ["jpg", "jpeg"],
            "certificate_format": ["pdf"]
        }
    
    @staticmethod
    def get_service_info() -> Dict[str, str]:
        """Get service information for display."""
        return {
            "name": "MPPSC Application",
            "full_name": "Madhya Pradesh Public Service Commission",
            "description": "Apply for MPPSC examinations",
            "category": "Recruitment"
        }
