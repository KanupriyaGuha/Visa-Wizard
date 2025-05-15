from datetime import timedelta
import json

# Function to load country-specific rules from a JSON file
def load_visa_rules(country):
    with open('data/visa_rules.json', 'r') as file:
        visa_rules = json.load(file)
    return visa_rules.get(country, {})

# Function to generate the timeline based on the visa type and country
def generate_timeline(graduation_date, visa_type, country):
    milestones = []
    visa_rules = load_visa_rules(country)

    if visa_type == "F1":
        milestones.append({"label": "OPT Application Window Opens", "date": graduation_date - timedelta(days=90)})
        milestones.append({"label": "Last Day to Apply for OPT", "date": graduation_date + timedelta(days=60)})
    elif visa_type == "STEM OPT":
        milestones.append({"label": "STEM OPT Application Opens", "date": graduation_date + timedelta(days=270)})
        milestones.append({"label": "STEM OPT Start Date", "date": graduation_date + timedelta(days=365)})
    elif visa_type == "H-1B":
        milestones.append({"label": "H-1B Lottery Registration Opens", "date": graduation_date + timedelta(days=300)})
        milestones.append({"label": "H-1B Work Start Date (If Selected)", "date": graduation_date + timedelta(days=450)})
    
    return milestones
