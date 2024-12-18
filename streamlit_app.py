import streamlit as st
import requests
import json
import uuid
from datetime import datetime


def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")

def save_current_chat():
    """Save current chat to chat history"""
    if st.session_state.messages:
        st.session_state.chat_history[st.session_state.current_chat_id] = {
            'messages': st.session_state.messages.copy(),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def start_new_chat():
    """Start a new chat session"""
    save_current_chat()
    st.session_state.messages = []
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.rerun()

def load_chat(chat_id):
    """Load a previous chat session"""
    if chat_id in st.session_state.chat_history:
        st.session_state.current_chat_id = chat_id
        st.session_state.messages = st.session_state.chat_history[chat_id]['messages'].copy()
        st.rerun()

def delete_chat(chat_id):
    """Delete a chat session"""
    if chat_id in st.session_state.chat_history:
        del st.session_state.chat_history[chat_id]
        if chat_id == st.session_state.current_chat_id:
            start_new_chat()
        else:
            st.rerun()

def send_message_to_endpoint(message):
    """
    Send message to the medical bot endpoint and get response
    Replace 'YOUR_API_ENDPOINT' with actual endpoint URL
    """
    try:

        global start_new
        
        #api_endpoint = "http://192.168.1.13:8000/api/chat"
        api_endpoint = "http://localhost:8000/api/chat"  # Update this line
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "timestamp": datetime.now().isoformat(),
            'session_id':  st.session_state.session_id,
            'message': message,
            'start_new':  st.session_state.start_new
        }
        print(payload)
        
        response = requests.post(
            api_endpoint,
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            if  st.session_state.start_new:
                 st.session_state.start_new=False
            return response.json()["response"]
        
        else:
            return "Sorry, I'm having trouble processing your request. Please try again."
        
        

            
    except Exception as e:
        return f"Error: Unable to get response from the medical bot. {str(e)}"
    

def main():
    # Page configuration
    st.set_page_config(
        page_title="Medical Assistant",
        page_icon="🏥",
        layout="wide"
    )

    # Initialize session state
    init_session_state()

    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if 'start_new' not in st.session_state:
        st.session_state.start_new = True

    # Create a container for the entire chat interface
    chat_container = st.container()

    # Sidebar remains the same
    with st.sidebar:
        st.title("💬 Chat History")
        
        # New Chat button at the top
        if st.button("🆕 Start New Chat", use_container_width=True):
            start_new_chat()
        
        st.divider()

        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### Previous Chats")
            for chat_id, chat_data in sorted(st.session_state.chat_history.items(), 
                                          key=lambda x: x[1]['timestamp'], 
                                          reverse=True):
                # Create a container for each chat entry
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    # Get first message of chat for preview
                    preview = chat_data['messages'][0]['content'] if chat_data['messages'] else "Empty chat"
                    preview = preview[:30] + "..." if len(preview) > 30 else preview
                    
                    # Display chat preview and timestamp
                    with col1:
                        if st.button(f"📝 {chat_data['timestamp']}\n{preview}", 
                                   key=f"load_{chat_id}",
                                   use_container_width=True):
                            load_chat(chat_id)
                    
                    # Delete button
                    with col2:
                        if st.button("🗑️", key=f"delete_{chat_id}"):
                            delete_chat(chat_id)
                
                st.divider()
        else:
            st.markdown("*No previous chats*")


    # Main chat interface using containers for better organization
    with chat_container:
        # Header container
        header_container = st.container()
        with header_container:
            st.title("🏥 Medical Assistant Chat")
            st.markdown("""
            Welcome! I'm your medical assistant chatbot. I can help you with:
            - General medical information
            - Symptom assessment
            - Health recommendations
            - Medical terminology explanations

            Please note that I'm not a replacement for professional medical advice.
            """)

        # File upload container
        upload_container = st.container()
        with upload_container:
            st.markdown("""
            <style>
            .uploadButton {
                opacity: 0.6;
                cursor: not-allowed;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📎 Upload Medical Documents")
            st.file_uploader(
                "Upload medical records or test results (Currently Disabled)", 
                type=["pdf", "jpg", "png"], 
                disabled=True,
                key="medical_docs"
            )
            st.markdown("""
            <div style='margin-bottom: 20px; color: gray; font-size: 0.8em;'>
            Document upload feature is currently disabled. Coming soon!
            </div>
            """, unsafe_allow_html=True)

        # Create a container for messages
        messages_container = st.container()

        # Create a container for input and disclaimer
        input_container = st.container()

        # Display chat messages in the messages container
        with messages_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Input and disclaimer in the input container
        with input_container:
            # Add some spacing before the input
            st.markdown("<br>" * 2, unsafe_allow_html=True)
            
            # Chat input
            if prompt := st.chat_input("Type your medical question here...", key="chat_input"):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown("Thinking...")
                    
                    response = send_message_to_endpoint(prompt)
                    message_placeholder.markdown(response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                # Save chat after each message
                save_current_chat()
                
                # Rerun to update the messages container
                st.rerun()

            # Disclaimer
            st.markdown("""
            ---
            **Disclaimer**: This chatbot is for informational purposes only and is not a substitute for professional medical advice, 
            diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions 
            you may have regarding a medical condition.
            """)

    # Add custom CSS to ensure proper layout
    st.markdown("""
        <style>
        .stChatFloatingInputContainer {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 60%;
            padding: 20px;
            background-color: white;
            z-index: 999;
        }
        .main {
            padding-bottom: 100px;
        }
        </style>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
