FROM python:3.9
WORKDIR /StickerService
COPY ./requirements.txt /StickerService/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /StickerService/requirements.txt
COPY . /StickerService
RUN chmod +x ./startup
CMD ["./startup"]