FROM python:3.9-slim

WORKDIR /app

COPY embedding.py .
RUN pip install --upgrade pip
RUN pip install sentence-transformers scikit-learn faiss-cpu

RUN python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2')"

CMD ["python", "embedding.py"]