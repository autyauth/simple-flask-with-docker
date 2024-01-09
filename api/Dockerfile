FROM python:3.7-alpine
WORKDIR /api
COPY requirements.txt /api/requirements.txt
RUN pip install -r /api/requirements.txt
COPY . .
CMD ["python", "app.py"]
