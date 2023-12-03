FROM python:3.8-alpine
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./app.py /app
COPY ./LocalController.py /app
COPY ./middleware.py /app
COPY ./monitor.py /app
COPY ./processor.py /app
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]