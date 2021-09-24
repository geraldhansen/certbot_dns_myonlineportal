FROM certbot/certbot

WORKDIR /certbot_dns_myonlineportal

COPY . .
RUN pip install .

