FROM python:3.10-slim
ENV PYTHONUNBUFFERED True

ARG MLFLOW_EXPERIMENT_NAME
ARG MLFLOW_TRACKING_USERNAME
ARG MLFLOW_TRACKING_PASSWORD
ARG MLFLOW_EXPERIMENT_TRACKING_URI

ENV PYTHONUNBUFFERED=True
ENV MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME
ENV MLFLOW_TRACKING_USERNAME=$MLFLOW_TRACKING_USERNAME
ENV MLFLOW_TRACKING_PASSWORD=$MLFLOW_TRACKING_PASSWORD
ENV MLFLOW_EXPERIMENT_TRACKING_URI=$MLFLOW_EXPERIMENT_TRACKING_URI
WORKDIR /usr/src/app
COPY ./serve-requirements.txt ./
RUN pip install --no-cache-dir -r serve-requirements.txt
COPY ./serve ./serve
EXPOSE 8080
CMD ["uvicorn", "serve.api:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
