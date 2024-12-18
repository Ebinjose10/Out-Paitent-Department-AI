# Out-Paitent-Department-AI
Out Patient Department (OPD) AI is a smart healthcare management system that combines artificial intelligence with traditional medical consultation workflows.


# Medical Assistant Cloud Run Application

A comprehensive medical assistant application that provides automated patient consultations, department recommendations, and appointment scheduling using Google Cloud Run and Gemini AI.

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
