from joblib import Parallel, delayed
from gensim import corpora
from gensim import models
from gensim.similarities import Similarity
from operator import itemgetter
import glob
import re
from typing import List
import spacy
import pickle

ENGLISH_DICT = r""
SPANISH_DICT = r""
STOPWORDS_SPANISH = r"resources/stopwords.txt"

class SymbolRemover():
    
    def __init__(self):
        self.replace_no_space = re.compile("(\&)|(\%)|(\$)|(\€)|(\.)|(\;)|(\:)|(\!)|(\')|(\¿)|(\¡)|(\!)|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)|(\⁰)|(\•)|(\\')")
        self.replace_space = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)|(\t)|(  )|(\n)")
    
    def execute(self, input_text) -> str:
        """
        Recibe un texto en crudo y elimina los caracteres que no aportan significado.
        Devuelve el texto en formato string en minúsculas.
        """
        returned = self.replace_no_space.sub("", input_text.lower())
        returned = self.replace_space.sub(" ", returned)       
        return returned

class Tokenizer():
    
    def __init__(self, component):
        self.component = component
    
    def execute(self, input_text) -> List[str]:
        """
        Recibe un texto y devuelve una lista de tokens.
        """
        output = self.component.execute(input_text)
        return output.split(" ")

class StopwordsRemover():
    
    def __init__(self, path, component):
        self.component = component
        self.stopwords = [line.strip() for line in open(path, "r", encoding = "utf-8").readlines()]
        
    def execute(self, input_text) -> List[str]:
        """
        Filtra los tokens eliminando aquellos que son palabras vacías.
        """
        tokens = self.component.execute(input_text)
        return [token for token in tokens if token not in self.stopwords]

class LemmatizerTagger():
    
    conversions = {
        "ADJ": "a",
        "ADV": "adv",
        "NOUN": "n",
        "NUM": "n",
        "PRON": "n",
        "PROPN": "n",
        "VERB": "v",
        "ADP": "prep",
        "JJ": "a",
        "JJR": "a",
        "JJS": "a",
        "NN": "n",
        "NNP": "n",
        "NNPS": "n",
        "NNS": "n",
        "RB": "adv",
        "RBR": "adv",
        "RBS": "adv",
        "RP": "adv",
        "VB": "v",
        "VBD": "v",
        "VBG": "v",
        "VBN": "v",
        "VBP": "v",
        "VBZ": "v",
    }
    
    def __init__(self, model, component):
        self.nlp = spacy.load(model)
        self.component = component
        
    def execute(self, input_text) -> List[str]:
        """
        Recibe una lista de tokens y devuelve sus lemas.
        """
        tokens = self.component.execute(input_text)
        returned = []
        for token in self.nlp(" ".join(tokens)):
            try:
                returned.append({
                    "lemma": token.lemma_,
                    "pos": self.conversions[token.tag_]
                })
            except:
                print(f"ERROR: {token} - {token.tag_}")
        return returned

class Eng2UNLTranslator():
    
    def __init__(self, file = "resources/eng2unl_ref.pickle"):
        with open(file, "rb") as f:
            self.dic = pickle.load(f)
            
    def get_combinations(self, tokens):
        """
        Calcula todas las combinaciones de los tokens dados.
        """
        result = [" ".join(tokens[i: j]) for i in range(len(tokens)) for j in range(i + 1, len(tokens) + 1) if j-i > 1]
        result.sort(reverse = True, key = len)
        return result
            
    def translate(self, tokens):
        """
        Recibe una lista de tokens en inglés lematizados (salida de lematizados) y devuelve una lista de uws.
        """
        print(f"\tQuery original = {tokens}")
        lemmas = [token["lemma"] for token in tokens]
        combinations = self.get_combinations(lemmas)
        
        translated = []
        
        for combination in combinations: # primero buscamos la uw de las expresiones en inglés
            if combination in self.dic:
                print(f"\t\tCombinación traducida {combination}")
                uws = [translation["uw"] for translation in self.dic[combination]]
                translated += uws
                
                # borramos las expresiones que tienen un lema ya traducido y los lemas traducidos
                combinations.remove(combination)
                for token in combination.split(" "):
                    for c in combinations: # combinaciones que quedan
                        if token in c: # la combinación tiene un lemma a traducido
                            combinations.remove(c)
                    lemmas.remove(token)

        # ahora traducimos los lemmas restantes
        for token in tokens:
            if token["lemma"] in lemmas: # no se ha traducido
                lemma = token["lemma"]
                if lemma in self.dic:
                    uws = [translation["uw"] for translation in self.dic[lemma] if translation["pos"] == token["pos"]]
                    translated += uws
                else:
                    print(f"\t\tNo se ha podido encontrar {lemma} en el diccionario Eng2UNL")
                
        print(f"\tUWs encontradas = {translated}")
        return translated

class UNL2EspTranslator():
    
    def __init__(self, file = "resources/unl2esp_ref.pickle"):
        with open(file, "rb") as f:
            self.dic = pickle.load(f)
            
    def get_combinations(self, tokens):
        """
        Calcula todas las combinaciones de los tokens dados.
        """
        result = [" ".join(tokens[i: j]) for i in range(len(tokens)) for j in range(i + 1, len(tokens) + 1) if j-i > 1]
        result.sort(reverse = True, key = len)
        return result
            
    def translate(self, uws):
        """
        Recibe una lista de uws y devuelve una lista de tokens en español.
        """
        print(f"\tUWs = {uws}")
        
        translated = []
        
        for uw in uws:
            if uw in self.dic:
                translations = [translation["lemma"] for translation in self.dic[uw]]
                translated += translations
            else:
                print(f"\t\tUW no encontrada en el diccionario de español: {uw}")
                
        print(f"\tTraducción al español = {translated}")
        return list(set(translated)) # para eliminar duplicados

class Translator():
    
    def __init__(self):
        self.eng2unl = Eng2UNLTranslator()
        self.unl2esp = UNL2EspTranslator()
        
    def translate(self, salida_preprocesado):
        print("Traduciendo a UNL...")
        uws = self.eng2unl.translate(salida_preprocesado)
        print("Traduciendo a ESP...")
        translations = self.unl2esp.translate(uws)
        return list(set(translations))

class MyCorpus:
        
    def __init__(self, docs, dictionary):
        self.docs = docs
        self.dictionary = dictionary

    def __iter__(self):
        for doc in self.docs:
            yield self.dictionary.doc2bow(doc)

class Indexer():       
    
    def __init__(self, path_docs = "documents/*/*.txt", dictionary = None, bow = None):
        self.pipeline = LemmatizerTagger("es_dep_news_trf", StopwordsRemover(STOPWORDS_SPANISH, Tokenizer(SymbolRemover())))
        self.repository = [open(doc, "r", encoding = "utf-8").read() for doc in glob.glob(path_docs)]
        if not (dictionary and bow):
            self.documents = Parallel(n_jobs = 12, verbose = 50)(delayed(self._preprocess_doc)(doc) for doc in glob.glob(path_docs))
        if dictionary:
            self.dictionary = corpora.Dictionary.load(dictionary)
        if bow:
            self.bow = corpora.MmCorpus(bow)
        
    def index(self):
        """
        Crea el diccionario de la colección y la bolsa de palabras.
        """
        self.dictionary = self._create_dictionary()
        self.dictionary.save("resources/dictionary.dict")
        self.bow = MyCorpus(self.documents, self.dictionary)
        corpora.MmCorpus.serialize("resources/bow.mm", self.bow)
        
    def _create_dictionary(self):
        """
        Función específica encargada de crear y guardar el diccionario.
        """
        dictionary = corpora.Dictionary(doc for doc in self.documents)
        return dictionary
        
    def _preprocess_doc(self, doc):
        with open(doc, "r", encoding = "utf-8") as f:
            content = f.read()
        return [token["lemma"] for token in self.pipeline.execute(content)]

class Searcher():
    
    def __init__(self, indexer):
        self.bow = indexer.bow
        self.dictionary = indexer.dictionary
        self.model = models.TfidfModel(self.bow)
        self.index = Similarity(None, corpus = indexer.bow, num_features = len(indexer.dictionary))
        self.pipeline_esp = LemmatizerTagger("es_dep_news_trf", Tokenizer(SymbolRemover()))
        self.pipeline_eng = LemmatizerTagger("en_core_web_trf", Tokenizer(SymbolRemover()))
        self.traductor = Translator()
        self.documents = indexer.repository
    
    def search(self, lang, query, k = 100, verbose = True):
        """
        En función del lenguaje, ejecuta una pipeline u otra y realiza la búsqueda.
        """
        if lang == "eng":
            pq = self.traductor.translate(self.pipeline_eng.execute(query))
            pq = [token for item in pq for token in item.split()]
        elif lang == "esp":
            pq = [token["lemma"] for token in self.pipeline_esp.execute(query)]
                        
        vq = self.dictionary.doc2bow(pq)
        qtfidf = self.model[vq]
        sim = self.index[qtfidf]
        ranking = sorted(enumerate(sim), key=itemgetter(1), reverse=True)

        returned = [
            {
                "document": self._bold(self.documents[doc].replace("\n", " "), query), 
                "score": "%.3f" % round(score,3)
            } for doc, score in ranking[:3] if score > 0
        ]

        return returned if returned else []

    def _bold(self, text, query):
        if re.match(query, text, re.IGNORECASE|re.DOTALL):
            print(1)
            text = re.sub(query, f"<b>{query} </b>", text, re.DOTALL|re.IGNORECASE)
        elif re.match(query[:-1], text, re.IGNORECASE|re.DOTALL):
            print(2)
            text = re.sub(query[:-1], f"<b>{query[:-1]} </b>", text, re.DOTALL|re.IGNORECASE)
        return text