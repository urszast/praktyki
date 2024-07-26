FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

RUN mkdir /tmp_multiproc

EXPOSE 8000

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# CMD ["gunicorn", "--bind", "0.0.0.0", "app:app"]
CMD ["gunicorn", "--bind", "teafrontend", "app:app"]
# CMD ["uvicorn", "--host", "0.0.0.0", "app:app"]