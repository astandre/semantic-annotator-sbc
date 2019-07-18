import spacy
# from flask import app
from rdflib import RDF
from sqlalchemy.orm import sessionmaker
from Models import *
import sqlalchemy as db
import rdflib
from flask import request
import os
from flask import Flask
from flask import render_template

dir_path = os.path.dirname(os.path.realpath(__file__))
nlp = spacy.load("es_core_news_sm")


# context = "Arroz Verde"
# # Adding default contexts
# if Context.check_context(session, context):
#     context_id = session.query(Context.id).filter(
#         Context.context == context).scalar()
# else:
#     context = Context(context=context)
#     session.add(context)
#     session.commit()
#     context_id = context.id

def clean_uri(uri):
    if uri.find('#') != -1:
        special_char = '#'
    else:
        special_char = '/'
    index = uri.rfind(special_char)
    return uri[index + 1:len(uri)]


print("Reading graph".center(30, "+"))
# Reading graph
grafo_av = rdflib.Graph()
# Nuestro archivo ttl
grafo_av.parse("data.rdf", format="xml")

app = Flask(__name__)

engine = db.create_engine('sqlite:///corruption.sqlite')

Base.metadata.create_all(engine)


@app.route("/")
def hello():
    return render_template("anotador.html", name="Hola")


@app.route("/anotate", methods=['POST'])
def annotate():
    print("Getting resources to annotate".center(30, "+"))
    if request.method == 'POST':
        text = request.json["text"]
        context_id = 1
        keywords = []
        cont_key = {}
        links = []
        # DB connection
        Session = sessionmaker(bind=engine)
        session = Session()
        #  Default context
        resources = session.query(Resource).filter(
            Resource.context_id == context_id, Resource.potential == False)
        for res in resources:
            for s, p, o in grafo_av.triples((None, None, rdflib.Literal(res.name))):
                keywords.append(res.name)
                links.append(s)
                query_result_graph = rdflib.Graph()
                query_result_graph += grafo_av.triples((s, None, None))
                # cont_key.update({res.name: res.type})

                for s2, p2, o2 in grafo_av.triples((s, RDF.type, None)):
                    # print(s2, p2, o2)
                    cont_key.update({res.name: clean_uri(o2)})

        list_sentences = []
        # for sentence in sentences:
        #   list_sentences.append(sentence.sentence)
        print("Converting text".center(30, "+"))
        text = nlp(text)
        for sent in text.sents:
            list_sentences.append(sent.text)
        print("Annotating".center(30, "+"))

        links_refinados = []
        for i in links:
            links_refinados.append(str(i).replace("http://localhost:8080/", "http://localhost:8080/sbc/page/"))

        dict_k = {}
        for i, j in zip(keywords, links_refinados):
            dict_k[i] = j

        #        list_sentences = []
        #        text = nlp(text)
        #        for sent in text.sents:
        #            list_sentences.append(sent.text)
        #        print("Annotating".center(30, "+"))
        #        dict_k = {}
        #        for i in keywords:
        #            dict_k[i] = i

        print("Resources used".center(30, "+"))

        print(dict_k)

        print("Keywords")

        print(keywords)
        print(len(keywords))

        print("Cont KEY")

        print(cont_key)
        print(len(cont_key))

        completa = ''.join(e for e in list_sentences)

        print("Count")
        # print(cont_key)
        res_count = {}
        entidades = {}
        for i, j in dict_k.items():
            conteo_entidad = completa.count(i)
            # print(i, conteo_entidad)
            if conteo_entidad > 0 and i in cont_key:
                print(cont_key[i], conteo_entidad, clean_uri(j))
                if cont_key[i] in res_count:
                    aux = res_count[cont_key[i]]
                    res_count.update({cont_key[i]: conteo_entidad + aux})
                    list_aux = entidades[cont_key[i]]
                    list_aux.append(clean_uri(j).replace("_", " "))
                    entidades.update({cont_key[i]: list_aux})
                else:
                    res_count.update({cont_key[i]: conteo_entidad})
                    entidades.update({cont_key[i]: [clean_uri(j).replace("_", " ")]})

        print(res_count)
        print(entidades)

        for i, j in dict_k.items():
            completa = completa.replace(i, "<a class='btn btn-success btn-sm' role='button' href=\"" + j + "\">" + i + "</a>")

        print("Appending info".center(30, "+"))
        print(completa)

        return {"data": completa, "count": res_count, "entidades": entidades}
    else:
        return {"error": "Method now allowed"}
