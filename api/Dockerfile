FROM ubuntu:18.04

RUN apt update -y

ENV TZ=Europe/Madrid

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=es_ES.UTF-8

ENV LANG es_ES.UTF-8 

RUN apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
  
RUN apt-get install libfreetype6-dev -y
RUN apt-get install pkg-config -y

RUN pip install gensim
RUN pip install spacy
RUN python -m spacy download en_core_web_trf
RUN python -m spacy download es_dep_news_trf
RUN pip install nltk
RUN pip install joblib
RUN pip install flask flask-cors

COPY . /app

WORKDIR /app

CMD ["python", "app.py"]