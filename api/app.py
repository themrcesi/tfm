"""from fastapi import FastAPI
from searcher import Searcher, Indexer

app = FastAPI()

dictionary = "resources/dictionary.dict"
bow = "resources/bow.mm"

indexer = Indexer(dictionary = dictionary, bow = bow)
searcher = Searcher(indexer = indexer)

@app.get("/queries")
def create_book(query: str, language: str):
    if language == "esp" or language == "eng":
        return searcher.search(language, query)
    return f"Idioma {language} incorrecto."
"""

# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_cors import CORS
import requests
from searcher import Searcher, Indexer
import json


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

dictionary = "resources/dictionary.dict"
bow = "resources/bow.mm"

indexer = Indexer(dictionary = dictionary, bow = bow)
searcher = Searcher(indexer = indexer)

@app.route('/queries', methods = ['GET'])
def chat():
    args = request.args
    if args["language"] == "esp" or args["language"] == "eng":
        return json.dumps(searcher.search(args["language"], args["query"]), ensure_ascii=False).encode('utf8'), 200
    return f"Idioma {args['language']} incorrecto.", 501


if __name__ == "__main__":
	CORS(app)
	app.run(host = "127.0.0.1", debug= False, port=6969, use_reloader=True)
