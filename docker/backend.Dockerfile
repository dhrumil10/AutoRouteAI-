FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first for caching
COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend source code
COPY ../autoroute-ai/ .

ENV MAPBOX_ACCESS_TOKEN=your_mapbox_token
ENV OPENAI_API_KEY=your_openai_key
ENV TOMTOM_API_KEY=your_tomtom_key

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
