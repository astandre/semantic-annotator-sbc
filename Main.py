import io
import spacy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models import *
from graph import *
import sqlalchemy as db

from decouple import config
import webbrowser
# from rdflib.namespace import RDF
# from rdflib import URIRef, BNode, Literal, Namespace, Graph
import pprint
import rdflib


nlp = spacy.load("es_core_news_sm")

engine = db.create_engine('sqlite:///resources.sqlite')

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

# Extraccion de informacion de HTML

# TODO extraer data de pagina web

ff = io.open("text.txt", 'r', encoding='utf-8')
text = ff.read()


# Identificacion de informacion
# ii = InformationIdentification(nlp, context_id, session)
# En este metodo se guardan las sentencias con las oraciones
## ii.handle_raw_data(text)

# Consultas de grafo:
g = Graph(nlp, context_id, session)
# g.draw()



# TODO anadir consultas de grafo

# Anotar semanticamente

def presente_triples(lista):
    for i in lista:
        print(i)

print(">>>>>>>>>>>>Most important nodes<<<<<<<<<<<<<<<<<")

grafo_av = rdflib.Graph()
grafo_av.parse("statements.ttl", format="ttl")
n = rdflib.Namespace(
    "https://mmisw.org/ont/?iri=http://www.arrozverde.org/ontology/")
resources = session.query(Resource).filter()
data = []
lista = ["Rafael Correa", "Jorge Glass"]

words = session.query(Word).filter()

list_text  = [text.split(' ')]


for word in list_text:
    text = []
    for s, p, o in grafo_av.triples((None, None, None)):
        text.append(o)
    for i in text:
        if(str(i).find(str(word))):
            print("Ok")
        # print(str(i).find("Lider"))
        # if t.find(word):
        #     for s, p, o in grafo_av.triples((None, None, rdflib.Literal(word))):
        #         query_result_graph = rdflib.Graph()
        #         query_result_graph += grafo_av.triples((s,None,None))
        #         lista_triple = [s, p, o in query_result_graph.triples((s, p, o))]
        #         for s,p,o in query_result_graph.triples((None,None,None)):
        #             print(s)
        #             print(o)

# for s, p, o in grafo_av:
#    if (None, None, rdflib.Literal(o)) not in g:
#        raise Exception("It better be!")

#resources = session.query(Resource).filter(Resource.context_id == context_id, Resource.potential == False)
#for res in resources:
#    print(res.name)
#     TODO Anadir aqui las consultas para generar el html


# for res in lista:
#     for s, p, o in grafo_av.triples((None, n['name'], rdflib.Literal(res))):
#         query_result_graph = rdflib.Graph()
#         query_result_graph += grafo_av.triples((s,None,None))
#         lista_triple = [s, p, o in query_result_graph.triples((s, p, o))]
#         data.append(query_result_graph)
#         f = open('/home/tony/repositorios/semantic-annotator-sbc/' + o + ".html", 'w')
#         message = """<html>
#                 <head></head>
#                 <body><h1>{0}</h1>
#                 <p>{1}</p>
#                 </body>
#                 </html>""".format(o, lista_triple)
#         f.write(message)
#         f.close()
#
#         semantic_ana = open('/home/tony/repositorios/semantic-annotator-sbc/seman.html', 'w')
#         message = """<html>
#                 <head></head>
#                 <body><h1>{0}</h1>
#                 <p>{1}</p>
#                 </body>
#                 # </html>""".format("Anotador Semantico", text)

