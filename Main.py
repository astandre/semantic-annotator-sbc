import spacy
from flask import app
from sqlalchemy.orm import sessionmaker
from Models import *
import sqlalchemy as db
from utils import dict_triples, formato_html
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

print("Reading graph".center(30, "+"))
# Reading graph
grafo_av = rdflib.Graph()
# Nuestro archivo ttl
grafo_av.parse("statements.rdf", format="xml")

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
        # DB connection
        Session = sessionmaker(bind=engine)
        session = Session()
        #  Default context
        resources = session.query(Resource).filter(
            Resource.context_id == context_id, Resource.potential == False)
        for res in resources:
            for s, p, o in grafo_av.triples((None, None, rdflib.Literal(res.name))):
                keywords.append(res.name)
                query_result_graph = rdflib.Graph()
                query_result_graph += grafo_av.triples((s, None, None))
                cont_key.update({res.name: res.type})
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

        list_sentences = []
        text = nlp(text)
        for sent in text.sents:
            list_sentences.append(sent.text)
        print("Annotating".center(30, "+"))
        dict_k = {}
        for i in keywords:
            dict_k[i] = i

        print("Resources used".center(30, "+"))

        print(dict_k)

        print("Keywords")

        print(keywords)
        print(len(keywords))

        print(cont_key)
        print(len(cont_key))

        completa = ''.join(e for e in list_sentences)

        print("Count")
        # print(cont_key)
        res_count = {}
        for i, j in dict_k.items():
            conteo_entidad = completa.count(i)
            # print(i, conteo_entidad)
            if conteo_entidad > 0 and i in cont_key:
                # print(cont_key[i], conteo_entidad)
                if cont_key[i] in res_count:
                    aux = res_count[cont_key[i]]
                    res_count.update({cont_key[i]: conteo_entidad + aux})
                else:
                    res_count.update({cont_key[i]: conteo_entidad})

        # TODO replace for real link to data
        link = "/repositorios/"

        for i, j in dict_k.items():
            completa = completa.replace(i, "<a href=\"" + link + i + ".html\">" + i + "</a>")

        print(res_count)
        print("Appending info".center(30, "+"))
        print(completa)
        #
        # try:
        #     index = open(dir_path + '/repositorios/index.html', 'w')
        # except IOError:
        #     index = open(dir_path + '/repositorios/index.html', 'x')
        #     index.close()
        #     print("Creating index.html".center(30, "+"))
        # styles = """
        #     h1{
        #         text-align: center;
        #         padding: 1em 0;
        #     }
        #     #cont_main{
        #         width: 90%;
        #         margin: auto;
        #         padding: 10px 20px;
        #         border: 1px solid #ccc;
        #     }
        #     #cont_main:hover{
        #         box-shadow: 0 0 3px rgba(89, 89, 89, 1);
        #     }
        # """
        #
        # message = """<html>
        #                     <head>
        #                         <meta charset="UTF-8">
        #                         <title>{0}</title>
        #                         <style>{1}</style>
        #                     </head>
        #                     <body>
        #                         <h1>{0}</h1>
        #                         <section id="cont_main">
        #                             <p>{2}</p>
        #                         </section>
        #                     </body>
        #                 </html>""".format("Anotador Semántico", styles, completa)
        # index.write(message)
        # index.close()

        return {"data": completa, "count": res_count}
    else:
        return {"error": "Method now allowed"}
