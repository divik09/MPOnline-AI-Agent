"""Service registry mapping service types to templates."""
from src.services.mppsc_template import MPPSCTemplate
from src.services.electricity_template import ElectricityTemplate, UniversityTemplate


# Central registry of all supported services
SERVICE_REGISTRY = {
    "mppsc": MPPSCTemplate,
    "electricity": ElectricityTemplate,
    "barkatullah": UniversityTemplate,
    "jiwaji": UniversityTemplate,
    "university": UniversityTemplate,
}


def get_service_list():
    """Get list of all available services with their info."""
    services = []
    
    for service_key, template_class in SERVICE_REGISTRY.items():
        info = template_class.get_service_info()
        services.append({
            "key": service_key,
            **info
        })
    
    return services


def get_service_template(service_type: str):
    """
    Get template class for a service type.
    
    Args:
        service_type: Service type key
        
    Returns:
        Template class or None
    """
    return SERVICE_REGISTRY.get(service_type)
