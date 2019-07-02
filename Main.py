import io
import spacy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models import *
from graph import *
from decouple import config

nlp = spacy.load("es_core_news_sm")

engine = create_engine(config('DATA_BASE'), echo=False, encoding='utf8', case_sensitive=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
context = "Arroz Verde"
# Adding default contexts
if Context.check_context(session, context):
    context_id = session.query(Context.id).filter(Context.context == context).scalar()
else:
    context = Context(context=context)
    session.add(context)
    session.commit()
    context_id = context.id

# Extraccion de informacion de HTML

# TODO extraer data de pagina web

ff = io.open("text.txt", 'r', encoding='utf-8')
text = ff.read()

# Anotar semanticamente

print(">>>>>>>>>>>>Most important nodes<<<<<<<<<<<<<<<<<")
resources = session.query(Resource).filter(Resource.context_id == context_id, Resource.potential == False)
for res in resources:
    print(res.name)
#     TODO Anadir aqui las consultas para generar el html


# Devolver reporte
