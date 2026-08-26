from data.training_data import UNIVERSITY_EXPERTISE

def match_university(category: str) -> str:
    return UNIVERSITY_EXPERTISE.get(category, "Unassigned")