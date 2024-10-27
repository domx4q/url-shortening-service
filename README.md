# Overview
This project is based on a [roadmap.sh](https://roadmap.sh/) project which can be found here: [https://roadmap.sh/projects/url-shortening-service](https://roadmap.sh/projects/url-shortening-service).
# Installation / Usage
1. Clone the repository
2. Run `pip install -r requirements.txt` (I am using Python 3.12)
3. Run `uvicorn main:app` to start the server
    - Uvicorn default to `http://127.0.0.1:8000` if the port is available
4. You can read the docs at `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`