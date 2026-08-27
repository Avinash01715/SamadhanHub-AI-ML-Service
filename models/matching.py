from data.training_data import UNIVERSITY_EXPERTISE

CATEGORY_DISPLAY_MAP = {
    "water_resources": "Agriculture & Water",
    "agriculture": "Agriculture & Water",
    "education": "Education & Skills",
    "healthcare": "Healthcare & Sanitation",
    "sanitation": "Healthcare & Sanitation",
    "urban_infra": "Urban & Rural Infrastructure",
    "environment": "Environment & Waste",
    "accessibility": "Livelihood & Tribal Empowerment",
}

RECOMMENDED_UNIVERSITIES = {
    "Agriculture & Water": ["Birsa Agricultural University (BAU) Ranchi", "BIT Sindri", "IIT (ISM) Dhanbad"],
    "Education & Skills": ["IIT (ISM) Dhanbad", "Vinoba Bhave University Hazaribagh", "NIT Jamshedpur"],
    "Healthcare & Sanitation": ["IIIT Ranchi", "Ranchi University", "BIT Sindri"],
    "Urban & Rural Infrastructure": ["BIT Sindri", "NIT Jamshedpur", "IIT (ISM) Dhanbad"],
    "Environment & Waste": ["IIT (ISM) Dhanbad", "BIT Sindri", "Ranchi University"],
    "Livelihood & Tribal Empowerment": ["Birsa Agricultural University (BAU) Ranchi", "Ranchi University", "IIIT Ranchi"],
}

def get_display_category(internal_category: str) -> str:
    return CATEGORY_DISPLAY_MAP.get(internal_category, internal_category)

def match_university(internal_category: str) -> str:
    return UNIVERSITY_EXPERTISE.get(internal_category, "Unassigned")

def get_recommended_universities(display_category: str) -> list:
    return RECOMMENDED_UNIVERSITIES.get(display_category, ["BIT Sindri", "IIT (ISM) Dhanbad"])