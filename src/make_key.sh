#!/bin/sh
openssl req -new -x509 -days 365 -nodes -out cert.pem -out ca.crt -keyout cert.pem
