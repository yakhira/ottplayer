FROM python:3.6-alpine

LABEL maintainer="Ruslan Yakhin <ruslan.k.yakhin@gmail.com>"

ENV WORKDIR /usr/src/app

WORKDIR $WORKDIR

RUN apk add --no-cache git bash gcc autoconf automake libtool libpng-dev musl-dev libffi-dev make mysql-client mysql-dev

COPY . $WORKDIR/

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["/usr/local/bin/python", "$WORKDIR/manage.py", "runserver"]
