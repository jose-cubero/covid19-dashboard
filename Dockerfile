FROM python:3.8

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt server.py ./
COPY covid19_dashboard/ covid19_dashboard/ 

# RUN pip install --no-cache-dir --upgrade pip \
RUN pip install -r requirements.txt

# Define environment variables for the dash server app
ENV dash_port=8050
ENV dash_debug="True"
CMD ["python", "server.py"]