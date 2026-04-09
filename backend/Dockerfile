FROM python:3.13

WORKDIR /app

COPY pyproject.toml .
RUN pip install .

COPY src ./src

EXPOSE 80

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]