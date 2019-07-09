import io
import spacy
from sqlalchemy.orm import sessionmaker
from Models import *
import sqlalchemy as db
from utils import dict_triples, formato_html
import rdflib
import webbrowser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
nlp = spacy.load("es_core_news_sm")

engine = db.create_engine('sqlite:///corruption.sqlite')

Base.metadata.create_all(engine)

# Create directory
try:
    # Create target Directory
    os.mkdir(dir_path + '/repositorios/')
    print("Directory /repositorios/ Created ")
except FileExistsError:
    print("Directory /repositorios/ Exists ")

# DB connection
Session = sessionmaker(bind=engine)
session = Session()

#  Default context
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

# Reading text to annotate
ff = io.open("text.txt", 'r', encoding='utf-8')
text = ff.read()

print("Reading graph".center(30, "+"))
# Reading graph
grafo_av = rdflib.Graph()
# Nuestro archivo ttl
grafo_av.parse("data.rdf", format="xml")

keywords = []
links =[]
print("Getting resources to annotate".center(30, "+"))
resources = session.query(Resource).filter(
    Resource.context_id == context_id, Resource.potential == False)
for res in resources:
    for s, p, o in grafo_av.triples((None, None, rdflib.Literal(res.name))):
        keywords.append(res.name)
        links.append(s)
        query_result_graph = rdflib.Graph()
        query_result_graph += grafo_av.triples((s, None, None))
        # lista_triple = [s, p, o in query_result_graph.triples((s, p, o))]
        # f = open(dir_path + '/repositorios/' + o + ".html",
        #          'w')
        # message = """<html>
        # <head></head>
        # <body>
        # <h1>{0}</h1>
        # {1}
        # </body>
        # </html>""".format(o, formato_html(dict_triples(query_result_graph)))
        # f.write(message)
        # f.close()

sentences = session.query(Sentence)
list_sentences = []
# for sentence in sentences:
#   list_sentences.append(sentence.sentence)
print("Converting text".center(30, "+"))
text = nlp(text)
for sent in text.sents:
    list_sentences.append(sent.text)
print("Annotating".center(30, "+"))

links_refinados=[]
for i in links:
    links_refinados.append(str(i).replace("http://localhost:8080/","http://localhost:8080/sbc/page/"))


dict_k = {}
for i,j in zip(keywords,links_refinados):
    dict_k[i] = j

print("Resources used".center(30, "+"))

print(dict_k)

print("\n")
# for i in list_sentences:
#     print(i)
completa = ''.join(e for e in list_sentences)



for i, j in dict_k.items():
    completa = completa.replace(i, "<a href=\"" + j + "\">" + i + "</a>")

print("Appending info".center(30, "+"))

try:
    index = open(dir_path + '/repositorios/index.html', 'w')
except IOError:
    index = open(dir_path + '/repositorios/index.html', 'x')
    index.close()
    print("Creating index.html".center(30, "+"))
styles = """
    h1{
        text-align: center;
        padding: 1em 0;
    }
    #cont_main{
        width: 90%;
        margin: auto;
        padding: 10px 20px;
        border: 1px solid #ccc;
    }
    #cont_main:hover{
        box-shadow: 0 0 3px rgba(89, 89, 89, 1);
    }
"""

message = """<html>
                    <head>
                        <meta charset="UTF-8">
                        <title>{0}</title>
                        <style>{1}</style>
                    </head>
                    <body>
                        <h1>{0}</h1>
                        <section id="cont_main">
                            <p>{2}</p>
                        </section>
                    </body>
                </html>""".format("Anotador Semántico",styles, completa)
index.write(message)
index.close()

filename = "/home/kfsarango1/repositorios/index.html"

print("Opening file".center(30, "+"))
filename = dir_path + "/repositorios/index.html"
webbrowser.open_new_tab(filename)
