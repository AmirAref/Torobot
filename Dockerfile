# pull the images
FROM python:3.11-alpine

# Set Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

# install the dependencies
COPY requirements.txt ./
RUN pip install -U pip && pip install -r requirements.txt

COPY . ./

CMD ["python", "bot.py"]