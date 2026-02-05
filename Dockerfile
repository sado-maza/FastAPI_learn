FROM python:3.14.2
WORKDIR /app

COPY . .


RUN pip install -r requirements.txt
CMD ["python","5authification.py"]

