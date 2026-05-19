FROM node:20-slim AS frontend
WORKDIR /frontend
COPY adjustment-front/TryingNewWorkspace/client/package*.json ./
RUN npm install
COPY adjustment-front/TryingNewWorkspace/client/ ./
RUN npm run build

FROM python:3.11-slim
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY --from=frontend /frontend/dist ./client/dist
EXPOSE 10000
CMD ["gunicorn", "-b", "0.0.0.0:10000", "run:app"]