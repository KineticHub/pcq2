FROM python:3.9
WORKDIR /SearchService
COPY ./SearchService/requirements.txt /SearchService/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /SearchService/requirements.txt
COPY ./SearchService /SearchService
RUN python manage.py migrate
RUN python manage.py migrate
CMD ["uvicorn", "SearchService.asgi:application", "--host", "0.0.0.0", "--port", "8118"]