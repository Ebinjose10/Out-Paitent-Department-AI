# Out-Paitent-Department-AI
Out Patient Department (OPD) AI is a smart healthcare management system that combines artificial intelligence with traditional medical consultation workflows.

please refer to medium article for more info:https://medium.com/@ebin97/opd-ai-transforming-medical-documentation-with-ai-b2eee75145a7

# Medical Assistant Cloud Run Application

A comprehensive medical assistant application that provides automated patient consultations, department recommendations, and appointment scheduling using Google Cloud Run and Gemini AI.

#OPD AI: Transforming Medical Documentation with AI

![image](https://github.com/user-attachments/assets/adb2ad63-1d23-4b2a-9369-2056b66a568c)

##Introduction

In India’s healthcare landscape, doctors face a critical challenge: spending up to 30% of their patient interaction time on documentation rather than care. With doctors seeing over 100 patients daily in just 6–8 hours, they’re left with only 3–5 minutes per consultation. OPD(out patient department) AI addresses this challenge by providing an intelligent medical documentation assistant that captures and structures patient interactions in real-time.

Target Audience: Healthcare providers, hospital administrators, and medical technology professionals looking to optimize their documentation workflow.

Expected Outcome: Understanding of how OPD AI can streamline medical documentation while improving patient care quality.

## Design

OPD AI employs a three-tier architecture designed for high-volume OPD environments:


![image](https://github.com/user-attachments/assets/e5643035-1100-4667-996e-b9168bfb3ce4)

## Design Rationale:
- Frontend using Streamlit: Chosen for its lightweight nature and minimal training requirements
- backend is a hosted on google clould run which provides auto-scalling capability hence it is flexible to use and simple to deploy using docker image
- Used cloud sql for data storage and retreval
- LLM Integration: used state of the art google Gemini 2.0 flash exp which Enables natural conversation processing and intelligent documentation

## Data Flow:
- Doctor-patient conversation captured through chat interface
- Real-time processing by LLM for medical terminology and context
- Automated generation of standardized medical reports
- Secure storage with EMR integration capability

## Prerequisites
- GCP account
- access to google Gemini 2.0 flash api
- google Cloud run access
- Google cloud sql

## Building Process

  The chat interface provides:

  - Real-time conversation capture
  - Medical terminology highlighting
  - Automatic formatting of patient information

### Setting Up the Chat Interface 
  
  ![image](https://github.com/user-attachments/assets/e746f17f-c455-4c90-aaeb-1ce689e365de)

  1.The chat interface provides:

  - Real-time conversation capture
  - Medical terminology highlighting
  - Automatic formatting of patient information

  2. Report Generation System

     ![image](https://github.com/user-attachments/assets/8ba54f41-0271-4a1e-bafb-3168d26491bd)

  The system automatically converts conversations into standardized medical reports:

    - Proper medical terminology usage
    - Consistent formatting
    - Comprehensive patient history integration

  3. Doctor Assignment Module

    Intelligent routing system that:

    - Analyzes patient symptoms
    - Checks doctor availability
    - Schedules appointments efficiently

## Results/Demo
![image](https://github.com/user-attachments/assets/6c8d70b2-77c7-4b00-938d-dcdcb279e439)
![image](https://github.com/user-attachments/assets/f9bcaab6-5fac-4d08-ac10-72011dc183a6)



## OPD AI demonstrates significant improvements in documentation efficiency:
  - 60% reduction in documentation time
  - Standardized format across departments
  - Improved patient data accessibility
  - Enhanced quality of medical records

## What’s Next
Future enhancements include:
- Integration with major EMR systems
- Multi-language support for regional healthcare
- Advanced document upload functionality
- Customizable templates for different specialties
- using google speech to text api for voice integration and also translation api for multi-language support
- integration with health apps
- Integration of multiple AI models (like X-ray detection,cancer prediction)
- document update from healthcare worker user

## Why Google Cloud?

OPD AI leverages Google Cloud’s robust infrastructure for:

  - Scalable computing resources
  - Secure data storage
  - Advanced AI/ML capabilities
  -Global availability and reliability



## Features
- Automated patient symptom collection
- AI-powered medical report generation
- Department recommendation system
- Automated appointment scheduling
- Cloud SQL integration for data persistence
- Real-time doctor availability checking

## Project Structure
```
├── docker-setup.py     # Docker configuration script
├── main.py            # Main application logic
├── server.py          # Flask server implementation
├── streamlit_app.py   # Streamlit frontend
├── requirements.txt   # Python dependencies
└── Dockerfile        # Docker configuration
```

## Prerequisites
- Python 3.9+
- Google Cloud account
- Cloud SQL instance
- Gemini AI API key

## Local Development Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export DB_USER=your_db_user
export DB_PASS=your_db_password
export DB_NAME=your_db_name
export GEMINI_API_KEY=your_api_key
```

## Docker Build and Deployment
1. Build Docker image:
```bash
docker build -t medical-assistant .
```

2. Run locally:
```bash
docker run -p 8000:8000 medical-assistant
```

3. Deploy to Cloud Run:
```bash
gcloud run deploy medical-assistant \
  --image gcr.io/ai-opd/medical-assistant \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Database Setup
The application requires a MySQL database. Schema setup scripts are provided in `docker-setup.py`.

## API Endpoints
- `/api/chat`: Main chat endpoint
- `/api/reset`: Reset session
- `/api/status`: Check service status

## Environment Variables
- `DB_USER`: Database username
- `DB_PASS`: Database password
- `DB_NAME`: Database name
- `GEMINI_API_KEY`: Gemini AI API key

## Database Setup
1. Rename `config_template.py` to `config.py`
2. Fill in your database credentials in `config.py`
3. Use `database_schema.sql` to create required tables
4. Do not commit `config.py` or any SQL files containing actual data

Note: The actual database credentials and connection parameters should be set through environment variables in production/Cloud Run.

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
MIT License
