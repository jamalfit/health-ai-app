FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 8080
CMD ["flask", "run", "--port=8080"]