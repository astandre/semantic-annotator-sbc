import io
import spacy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models import *
from graph import *
import sqlalchemy as db
import webbrowser
from utils import dict_triples, formato_html
import re
import rdflib
import webbrowser

nlp = spacy.load("es_core_news_sm")

engine = db.create_engine('sqlite:///corruption.sqlite')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
context = "Arroz Verde"
# Adding default contexts
if Context.check_context(session, context):
    context_id = session.query(Context.id).filter(
        Context.context == context).scalar()
else:
    context = Context(context=context)
    session.add(context)
    session.commit()
    context_id = context.id

ff = io.open("text.txt", 'r', encoding='utf-8')
text = ff.read()

# Identificacion de informacion
# ii = InformationIdentification(nlp, context_id, session)
# En este metodo se guardan las sentencias con las oraciones
# ii.handle_raw_data(text)

# Consultas de grafo:
g = Graph(nlp, context_id, session)


# g.draw()


# TODO anadir consultas de grafo

# Anotar semanticamente

print(">>>>>>>>>>>>Most important nodes<<<<<<<<<<<<<<<<<")
# declaro la clase grafo para poder consultar el grafo
grafo_av = rdflib.Graph()
# Nuestro archivo ttl
grafo_av.parse("statements.rdf", format="xml")

keywords = []

resources = session.query(Resource).filter(
    Resource.context_id == context_id, Resource.potential == False)
for res in resources:
    for s, p, o in grafo_av.triples((None, None, rdflib.Literal(res.name))):
        keywords.append(res.name)
        query_result_graph = rdflib.Graph()
        query_result_graph += grafo_av.triples((s, None, None))
        #lista_triple = [s, p, o in query_result_graph.triples((s, p, o))]
        f = open('/home/tony/repositorios/' + o + ".html", 'w')
        message = """<html>
        <head></head>
        <body>
        <h1>{0}</h1>
        {1}
        </body>
        </html>""".format(o, formato_html(dict_triples(query_result_graph)))
        f.write(message)
        f.close()


sentences = session.query(Sentence)
list_sentences = []
# for sentence in sentences:
#   list_sentences.append(sentence.sentence)

text = nlp(text)
for sent in text.sents:
    list_sentences.append(sent.text)


dict_k = {}
for i in keywords:
    dict_k[i] = i

print(dict_k)
print("\n")
# for i in list_sentences:
#     print(i)
completa = ''.join(e for e in list_sentences)
link = "/home/tony/repositorios/"
for i, j in dict_k.items():
    completa = completa.replace(i, "<a href=\""+link+i+".html\">"+i+"</a>")
print(completa)

index = open('/home/tony/repositorios/index.html', 'w')
message = """<html>
                <head></head>
                <body><h1>{0}</h1>
                <p>{1}</p>
                </body>
                # </html>""".format("Anotador Semántico", completa)
index.write(message)
index.close()
filename = "/home/tony/repositorios/index.html"
webbrowser.open_new_tab(filename)
