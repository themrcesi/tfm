FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install gensim
RUN pip install spacy
RUN python -m spacy download en_core_web_trf
RUN python -m spacy download es_dep_news_trf
RUN pip install nltk
RUN pip install joblib

COPY . /app

WORKDIR /app

CMD uvicorn app:app --port 6969