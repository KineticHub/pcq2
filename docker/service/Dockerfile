FROM python:3.9
WORKDIR /StickerService
COPY ./StickerService/requirements.txt /StickerService/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /StickerService/requirements.txt
COPY ./StickerService /StickerService
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
CMD ["uvicorn", "StickerService.asgi:application", "--host", "0.0.0.0", "--port", "8000"]