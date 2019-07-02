from bs4 import BeautifulSoup
from requests_html import HTMLSession
from information_identification import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import spacy
from decouple import config

nlp = spacy.load("es_core_news_sm")
engine = create_engine(config('DATA_BASE'), echo=False, encoding='utf8', case_sensitive=True)
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

session_html = HTMLSession()

r = session_html.get(
    "https://milhojas.is/612540-odebretch-y-otras-multinacionales-pusieron-presidente-en-ecuador.html")
raw = r.html.html

soup = BeautifulSoup(raw, 'html.parser')
print(soup.get_text())

# Identificacion de informacion
ii = InformationIdentification(nlp, context_id, session)
# En este metodo se guardan las sentencias con las oraciones
ii.handle_raw_data("")
