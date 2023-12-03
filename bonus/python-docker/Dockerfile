FROM python:3.8-alpine
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN apk --no-cache add curl
COPY ./app.py /app/app.py
COPY ./LocalController.py /app/LocalController.py
COPY ./middleware.py /app/middleware.py
COPY ./processor.py /app/processor.py
COPY script.sh /app/script.sh
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin
RUN chmod +x /app/script.sh
ENTRYPOINT ["/app/script.sh"]
CMD /bin/bash