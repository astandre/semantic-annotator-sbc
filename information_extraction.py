from bs4 import BeautifulSoup
from requests_html import HTMLSession
from information_identification import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import spacy
from decouple import config
import re
import sqlalchemy as db


nlp = spacy.load("es_core_news_sm")

engine = db.create_engine('sqlite:///corruption.sqlite')

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

session_html = HTMLSession()

links = ["https://milhojas.is/612540-odebretch-y-otras-multinacionales-pusieron-presidente-en-ecuador.html",
         'https://milhojas.is/612541-todos-los-nombres-de-arroz-verde.html']

for link in links:
    print("Searching for %s" % link)

    r = session_html.get(link)
    raw = r.html.html

    soup = BeautifulSoup(raw, 'html.parser')
    # raw_text = soup.get_text()

    # print(raw_text)

    # print(soup.find_all('strong'))
    #
    potential_res = [value.string for value in soup.find_all('strong')]

    print("Adding potential res".center(30, "+"))

    print(potential_res)
    # custom_stop_words = ["\xa0", " "]
    # Adding potential res:
    for pot_res in potential_res:
        print(pot_res)
        # if pot_res not in custom_stop_words or pot_res is not None or pot_res.find("$") != -1:
        #     print(pot_res)
        #     resource = Resource(name=pot_res, type="W", potential=True, context_id=context_id)
        #     session.add(resource)

    # session.commit()

    raw_text = soup.find(id="maininner").get_text()

    print(raw_text)
    print("Length ", len(raw_text))

    print("Cleaning data".center(30, "+"))

    raw_text = raw_text.replace('\n', ' ')
    raw_text = raw_text.replace('“', '')
    raw_text = raw_text.replace('”', '')
    raw_text = re.sub(' +', ' ', raw_text)

    print(raw_text)
    print("Length ", len(raw_text))
    # for script in soup.find_all("script"):
    #     script.extract()

    # Identificacion de informacion
    ii = InformationIdentification(nlp, context_id, session)
    # En este metodo se guardan las sentencias con las oraciones

    print("Sentences found".center(30, "+"))
    data = nlp(raw_text)

    for sentence in data.sents:
        ii.handle_sentences(sentence.text)

    sentences = session.query(Sentence).filter(Sentence.context_id == context_id)

    print("Entities found!".center(30, "+"))

    ii.get_entities(sentences)
