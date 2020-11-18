FROM python:3

MAINTAINER joshua


WORKDIR .

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python","-u", "./main.py" ]