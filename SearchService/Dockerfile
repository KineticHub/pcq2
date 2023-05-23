FROM python:3.9
WORKDIR /SearchService
COPY ./requirements.txt /SearchService/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /SearchService/requirements.txt
COPY . /SearchService
RUN chmod +x ./startup
CMD ["./startup"]