FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file first, for separate dependency resolving and downloading
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application's code
COPY . /app
WORKDIR /app
# Make the entrypoint a terminal
#CMD ["/bin/bash"]
CMD ["python", "main.py", "--video_id_file","video_ids.txt"]