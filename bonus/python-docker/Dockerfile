FROM python:3.8-alpine
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./app.py /app/app.py
COPY ./LocalController.py /app/LocalController.py
COPY ./middleware.py /app/middleware.py
COPY ./monitor.py /app/monitor.py
COPY ./processor.py /app/processor.py
COPY script.sh /app/script.sh
RUN chmod +x /app/script.sh
ENTRYPOINT ["/app/script.sh"]