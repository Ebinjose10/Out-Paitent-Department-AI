# config_template.py
# Rename this file to config.py and fill in your actual values

# Database Configuration
DB_CONFIG = {
    "local": {
        "host": "localhost",
        "user": "your_username",
        "password": "your_password",
        "database": "hospital_db"
    },
    "cloud": {
        "instance_connection_name": "project:region:instance",
        "user": "your_cloud_sql_username",
        "password": "your_cloud_sql_password",
        "database": "hospital_db"
    }
}

# API Keys
GEMINI_API_KEY = "your_gemini_api_key"

# Slot Times Configuration
SLOT_TIMES = {
    'slot_1': '9:00 AM',
    'slot_2': '10:00 AM',
    'slot_3': '11:00 AM',
    'slot_4': '12:00 PM',
    'slot_5': '2:00 PM',
    'slot_6': '3:00 PM',
    'slot_7': '4:00 PM',
    'slot_8': '5:00 PM'
}

# Department Mapping
DEPARTMENTS = {
    'general_medicine': 'Primary care and general health issues',
    'cardiology': 'Heart and cardiovascular system',
    'neurology': 'Brain and nervous system',
    'gastroenterology': 'Digestive system',
    'pulmonology': 'Respiratory system',
    'endocrinology': 'Hormonal disorders',
    'orthopedics': 'Bone and joint issues'
}
