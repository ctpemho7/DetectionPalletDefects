FROM python:3.10
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN apt update && \
    apt install -y \
      python3-pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src
CMD ["fastapi", "run", "./src/daemon/daemon.py", "--port", "8000"]
