certbot-dns-myonlineportal
============

MyOnlinePortal DNS Authenticator plugin for [Certbot](https://certbot.eff.org/).

This plugin is built from the ground up and follows the development style and life-cycle
of other `certbot-dns-*` plugins found in the
[Official Certbot Repository](https://github.com/certbot/certbot).

Installation
------------

```
pip install --upgrade certbot
pip install certbot-dns-myonlineportal
```

Verify:

```
$ certbot plugins --text

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
* dns-myonlineportal
Description: Obtain certificates using a DNS TXT record (if you are using
MyOnlinePortal for DNS).
Interfaces: Authenticator, Plugin
Entry point: dns-myonlineportal =
certbot_dns_myonlineportal.dns_myonlineportal:Authenticator

...
...
```

Configuration
-------------

The credentials file e.g. `~/myonlineportal-credentials.ini` should look like this:

```
certbot_dns_myonlineportal:dns_myonlineportal_username = username
certbot_dns_myonlineportal:dns_myonlineportal_password = password
certbot_dns_myonlineportal:dns_myonlineportal_endpoint = https://myonlineportal.net/set-acme
```

Usage
-----

```
certbot ... \
        --authenticator certbot-dns-myonlineportal:dns-myonlineportal \
        --certbot-dns-myonlineportal:dns-myonlineportal-propagation-seconds 90 \
        --certbot-dns-myonlineportal:dns-myonlineportal-credentials ~/myonlineportal-credentials.ini \
        certonly
```

Development
-----------

Build the docker container
```
docker build -t certbot/dns-myonlineportal .
```

Run the docker container
```
mkdir -p ./var/lib/letsencrypt
mkdir -p ./var/log/letsencrypt
mkdir -p ./etc/letsencrypt
PWD=$(pwd)

docker run \
  --rm \
  -v ${PWD}/var/lib/letsencrypt:/var/lib/letsencrypt \
  -v ${PWD}/var/log/letsencrypt:/var/log/letsencrypt \
  -v ${PWD}/etc/letsencrypt:/etc/letsencrypt \
  --cap-drop=all \
  certbot/dns-myonlineportal certonly --debug \
   --authenticator certbot-dns-myonlineportal:dns-myonlineportal \
   --certbot-dns-myonlineportal:dns-myonlineportal-propagation-seconds 90 \
   --certbot-dns-myonlineportal:dns-myonlineportal-credentials ~/myonlineportal-credentials.ini \
   --no-self-upgrade \
   --agree-tos \
   --email 'my.email@example.com' \
   --keep-until-expiring --non-interactive --expand \
   --server https://acme-v02.api.letsencrypt.org/directory \
   -d example.myonlineportal.net -d '*.example.myonlineportal.net'

```

Run the tests
```
python3 setup.py test
```

Build the package
```
python3 -m build
```

Upload to pypi
```
python3 -m twine upload --repository testpypi dist/*
```

Helpful links
--------

[MyOnlinePortal api](https://myonlineportal.net/help#acme_api)
