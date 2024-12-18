import multiprocessing
from streamlit_app import main as streamlit_main  # Imports your Streamlit app's main function
from server import app as flask_app  # Imports your Flask app

def run_streamlit():
    """
    Function to run the Streamlit server.
    Uses Streamlit's CLI to run the app with specific configuration.
    """
    import streamlit.web.cli as stcli
    import sys
    
    # Configure Streamlit command line arguments
    sys.argv = [
        "streamlit",  # Command
        "run",        # Action
        "streamlit_app.py",  # Your Streamlit app file
        "--server.port", "8501",  # Port to run Streamlit on
        "--server.address", "0.0.0.0"  # Allow external connections
    ]
    sys.exit(stcli.main())

def run_flask():
    """
    Function to run the Flask server.
    """
    flask_app.run(host='0.0.0.0', port=8000)

if __name__ == '__main__':
    # Create separate processes for each application
    streamlit_process = multiprocessing.Process(target=run_streamlit)
    flask_process = multiprocessing.Process(target=run_flask)
    
    # Start both processes
    streamlit_process.start()
    flask_process.start()
    
    # Wait for both processes to complete
    streamlit_process.join()
    flask_process.join()
