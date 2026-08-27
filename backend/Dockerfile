FROM python:3.11-slim

ENV PYTHONUNBUFFERED=True

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir Feature_Engineering

COPY CORE ./CORE
COPY ./Training_Model ./Training_Model
COPY ./Feature_Engineering/utils/selection ./Feature_Engineering
COPY ./Feature_Engineering/utils/transformers ./Feature_Engineering
COPY ./Feature_Engineering/utils/__init__.py ./Feature_Engineering
COPY ./src ./src
COPY ./logs ./logs
COPY ./.env ./

ENV PYTHONPATH=/usr/src/app

EXPOSE 8082

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8082"]
