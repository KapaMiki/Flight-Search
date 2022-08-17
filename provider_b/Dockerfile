FROM python:3.7

ENV PYTHONUNBUFFERED=1 COLUMNS=200 TZ=Asia/Almaty
WORKDIR /app
RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY project/ .
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
