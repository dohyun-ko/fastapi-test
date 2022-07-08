FROM python:3.10

COPY . .

WORKDIR .

RUN pip install -r /recommend/requirements.txt

EXPOSE 8000

CMD ["python", "-m", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--access-logfile", "./gunicorn-access.log", "recommend.main:app", "--bind", "0.0.0.0:8000", "--workers", "2"]