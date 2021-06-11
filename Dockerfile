FROM python:3.8
WORKDIR /app
COPY . /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "main_bot.py"]
