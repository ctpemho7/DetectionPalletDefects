FROM python:3.10

COPY ./requirements.txt /
RUN apt update && \
    apt install -y python3-pip
# libglib2.0-0 libsm6 libxrender1 libxext6 libgl1-mesa-dev

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ADD ./src /src
WORKDIR /src
CMD ["fastapi", "run", "./daemon/daemon.py", "--reload", "--port", "8000"]
