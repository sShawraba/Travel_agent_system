FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml .

# Install dependencies using uv
RUN uv pip install --system fastapi uvicorn pydantic pydantic-settings langchain langchain-google-genai langgraph langsmith scikit-learn joblib python-dotenv

# Copy application code
COPY backend/app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
