FROM python:3.10-slim-buster


RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    git \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    make \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file first, for separate dependency resolving and downloading
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application's code
COPY . /app
WORKDIR /app

CMD ["python", "main.py"]