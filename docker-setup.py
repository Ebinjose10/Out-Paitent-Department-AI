# main.py
import multiprocessing
from streamlit_app import main as streamlit_main
from server import app as flask_app

def run_streamlit():
    import streamlit.web.cli as stcli
    import sys
    
    sys.argv = ["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
    sys.exit(stcli.main())

def run_flask():
    flask_app.run(host='0.0.0.0', port=8000)

if __name__ == '__main__':
    # Create process for Streamlit
    streamlit_process = multiprocessing.Process(target=run_streamlit)
    # Create process for Flask
    flask_process = multiprocessing.Process(target=run_flask)
    
    # Start both processes
    streamlit_process.start()
    flask_process.start()
    
    # Wait for both processes to complete
    streamlit_process.join()
    flask_process.join()
