FROM python:3.12

COPY requirements.txt /home/ubuntu/fast_api/
WORKDIR /home/ubuntu/fast_api
RUN pip install -r requirements.txt

COPY . /home/ubuntu/fast_api/

EXPOSE 80

CMD ["uvicorn", "main:app", "--workers", "8", "--host", "0.0.0.0", "--port", "80", "--timeout-keep-alive", "600"]
