import subprocess
import sys
import time
import threading

def run_fastapi():
    """Run FastAPI server"""
    subprocess.run([sys.executable, "-m", "uvicorn", "api:app", "--reload", "--port", "8000", "--host", "0.0.0.0"])

def run_streamlit():
    """Run Streamlit app"""
    time.sleep(5)  # Wait for FastAPI to start
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.host", "0.0.0.0"])

if __name__ == "__main__":
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()
    
    # Start Streamlit in main thread
    run_streamlit()