FROM python:3.10-slim-buster

LABEL maintainer="Ad.BadiDesign@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./core/requirements.txt .
COPY ./core/entrypoint.sh .
COPY ./core .
RUN chmod +x ./entrypoint.sh

# RUN pip config --user set global.index https://mirror-pypi.runflare.com/simple && pip config --user set global.index-url https://mirror-pypi.runflare.com/simple && pip config --user set global.trusted-host mirror-pypi.runflare.com
RUN pip install --upgrade pip && pip install -r requirements.txt


EXPOSE 8000

# execute our entrypoint.sh file
CMD ["sh","./entrypoint.sh"]