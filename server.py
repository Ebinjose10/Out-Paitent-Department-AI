# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)
CORS(app)

class OPDChatbot:
    def __init__(self, api_key):
        # Initialize Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Streamlined department information
        self.departments = {
            'general_medicine': 'Primary care and general health issues',
            'cardiology': 'Heart and cardiovascular system',
            'neurology': 'Brain and nervous system',
            'gastroenterology': 'Digestive system',
            'pulmonology': 'Respiratory system',
            'endocrinology': 'Hormonal disorders',
            'orthopedics': 'Bone and joint issues'
        }
        
        # Initialize chat history and assessment state
        self.chat_history = []
        self.assessment_stage = 0
        self.patient_data = {
            'symptoms': [],
            'duration': '',
            'severity': '',
            'medical_history': '',
            'current_medications': '',
            'lifestyle_factors': '',
            'family_history':''
        }
        
        # Assessment questions for structured conversation
        self.assessment_questions = [
            "Please describe your main symptoms in detail.",
            "How long have you been experiencing these symptoms?",
            "Are you currently taking any medications? Please list them.",
            "Do you have any previous medical conditions or surgeries?",
            "Please describe your lifestyle (smoking, alcohol, exercise, diet).",
            "any family history relevant to this case"
        ]

    def get_next_assessment_question(self):
        if self.assessment_stage < len(self.assessment_questions):
            return self.assessment_questions[self.assessment_stage]
        return None

    def suggest_tests(self, symptoms, medical_history):
        test_prompt = f"""
        Based on the following patient information:
        Symptoms: {symptoms}
        Medical History: {medical_history}
        
        Suggest relevant medical tests and investigations in order of priority.
        Consider:
        1. Basic vital tests (BP, temperature, etc.)
        2. Blood tests
        3. Imaging (X-ray, MRI, CT scan, etc.)
        4. Specialized tests
        
        Return a structured list of recommended tests with brief justifications.
        """
        response = self.model.generate_content(test_prompt)
        return response.text

    def generate_medical_report(self, symptoms, medical_history):
        report_prompt = f"""
        Generate a comprehensive medical report based on the following information:
        
        Patient Information:
        - Symptoms: {', '.join(self.patient_data['symptoms'])}
        - Duration: {self.patient_data['duration']}
        - Medical History: {self.patient_data['medical_history']}
        - Current Medications: {self.patient_data['current_medications']}
        - Lifestyle Factors: {self.patient_data['lifestyle_factors']}
        - Family history: {self.patient_data['family_history']}
        
        also Based on the following patient information:
        Symptoms: {symptoms}
        Medical History: {medical_history}
        
        Suggest relevant medical tests and investigations in order of priority.
        Consider:
        1. Basic vital tests (BP, temperature, etc.)
        2. Blood tests
        3. Imaging (X-ray, MRI, CT scan, etc.)
        4. Specialized tests

        Generate a detailed medical report in markdown format following these exact specifications:

        1. FORMAT REQUIREMENTS:
        - Use level 1 heading (#) only for the title "MEDICAL REPORT"
        - Use level 2 headings (##) for main sections
        - Use asterisks (*) for all bullet points
        - Use proper markdown table syntax with alignment pipes
        - Ensure proper spacing between sections (one blank line)
        - Use bold (**text**) for important findings or values
        - Use italics (*text*) for medical terminology or emphasis

        2. REQUIRED SECTIONS (in order):
        a) Title: "MEDICAL REPORT"
        b) Patient Information (without heading):
        - Patient Name: [Name]
        - Date: [Date]
        - Medical Record Number: [MRN]

        c) Main sections (with ## headings):
        1. Chief Complaints
        2. History of Present Illness
        3. Past Medical History
        4. Physical Examination
        5. Assessment
        6. Plan & Recommendations

        3. LISTS AND BULLET POINTS:
        - Use single asterisk (*) for all bullet points
        - Maintain consistent indentation for nested lists
        - Add space after each asterisk

        4. TABLE REQUIREMENTS:
        - Use proper markdown table syntax
        - Include header row
        - Use alignment indicators (---)
        - Example:
        |Parameter|Value|
        |---------|-----|
        |Content  |Data |

        5. FORMATTING RULES:
        - Bold (**) for critical values
        - Italics (*) for medical terms
        - One blank line between sections
        - Proper spacing after headers
        - Consistent capitalization

        Please generate a medical report following these specifications, using the following clinical information.
        Format the report professionally and concisely.
        """
        response = self.model.generate_content(report_prompt)
        return response.text

    def get_response(self, user_input):
        # Store user input in chat history
        self.chat_history.append({"role": "user", "content": user_input})
        
        # Process user input based on current assessment stage
        if self.assessment_stage < len(self.assessment_questions):
            # Update patient data based on current stage
            if self.assessment_stage == 0:
                self.patient_data['symptoms'].append(user_input)
            elif self.assessment_stage == 1:
                self.patient_data['duration'] = user_input
            elif self.assessment_stage == 2:
                self.patient_data['current_medications'] = user_input
            elif self.assessment_stage == 3:
                self.patient_data['medical_history'] = user_input
            elif self.assessment_stage == 4:
                self.patient_data['lifestyle_factors'] = user_input
            elif self.assessment_stage == 5:
                self.patient_data['family_history'] = user_input
            
            self.assessment_stage += 1
            
            # If assessment is complete, generate final report
            if self.assessment_stage >= len(self.assessment_questions):
                medical_report = self.generate_medical_report(
                    self.patient_data['symptoms'],
                    self.patient_data['medical_history']
                )
                response = medical_report
            else:
                # Get next assessment question
                next_question = self.get_next_assessment_question()
                response = f"Thank you. {next_question}"
        
        # Store assistant response in chat history
        self.chat_history.append({"role": "assistant", "content": response})
        return response

# Initialize chatbot instances for different sessions
chatbot_sessions = {}

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        session_id = data.get('session_id')
        message = data.get('message')
        start_new = data.get('start_new', False)
        
        # Create new session or get existing one
        if start_new or session_id not in chatbot_sessions:
            chatbot_sessions[session_id] = OPDChatbot(api_key="ENTER YOUR API KEY HERE")
            response = "Hello! I'll help assess your condition through a series of questions. Please describe your main symptoms."
            return jsonify({
                'response': response,
                'is_first': True,
                'is_end': False,
                'status': 'success'
            })
        
        # Get existing chatbot instance
        chatbot = chatbot_sessions[session_id]
        
        # Process message
        response = chatbot.get_response(message)
        
        # Check if assessment is complete
        is_end = chatbot.assessment_stage >= len(chatbot.assessment_questions)
        
        return jsonify({
            'response': response,
            'is_first': False,
            'is_end': is_end,
            'status': 'success',
            'chat_history': chatbot.chat_history  # Added to include chat history
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_session():
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id in chatbot_sessions:
            del chatbot_sessions[session_id]
        
        return jsonify({
            'status': 'success',
            'message': 'Session reset successfully'
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'status': 'running',
        'active_sessions': len(chatbot_sessions)
    })

if __name__ == '__main__':
    #app.run(debug=True, port=8000)
    app.run(debug=True, host='0.0.0.0', port=8000)
