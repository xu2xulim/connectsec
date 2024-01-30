FROM python:3.9-slim
WORKDIR /tg_bot
COPY /alert/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "alert.main:app", "--host", "0.0.0.0", "--port", "8000"]