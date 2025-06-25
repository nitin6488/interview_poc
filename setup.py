from setuptools import setup, find_packages

setup(
    name="interview-research-assistant",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.28.0",
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "pymongo==4.5.0",
        "requests==2.31.0",
        "beautifulsoup4==4.12.2",
        "google-generativeai==0.3.2",
        "langchain==0.0.335",
        "langchain-google-genai==0.0.6",
        "selenium==4.15.0",
        "python-dotenv==1.0.0",
        "pydantic==2.4.2",
        "motor==3.3.2",
        "aiohttp==3.9.0",
        "plotly==5.17.0",
        "pandas==2.1.3"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered interview research assistant",
    python_requires=">=3.8",
)