from Models import *
from sqlalchemy import update


class InformationIdentification:
    def __init__(self, nlp, context_id, session):
        self.nlp = nlp
        self.context_id = context_id
        self.session = session

    def handle_sentences(self, sentence):
        print("SENTECE: ", sentence)
        new_sentence = Sentence(sentence=sentence, context_id=self.context_id)
        self.session.add(new_sentence)
        self.session.commit()
        sentence = self.nlp(sentence)
        order = 0
        for token in sentence:
            word = token.text
            if not token.is_stop and token.is_punct is False and token.pos_ != "SPACE":
                print("WORD: %s | POS: %s | LEMMA: %s" % (word, token.pos_, token.lemma_))
                new_word = Word(word=word, pos=token.pos_, order=order, lemma=token.lemma_,
                                sentence_id=new_sentence.id)
                self.session.add(new_word)
                order += 1
        self.session.commit()

    def handle_raw_data(self, text):
        data = self.nlp(text)
        for i, token in enumerate(data.sents):
            self.handle_sentences(token.text)

    def get_entities(self, sentences):
        for sent in sentences:
            doc = self.nlp(sent.sentence)
            for ent in doc.ents:
                print(ent.text, ent.label_)
                if ent.label_ != "None" and not Resource.check_resource(self.session, ent.text, self.context_id):
                    print("Resource %s not found!" % ent.text)
                    resource = Resource(name=ent.text, type=ent.label_, context_id=self.context_id, potential=True)
                    self.session.add(resource)
                else:
                    print("Resource  %s found! Updating" % ent.text)
                    resource = self.session.query(Resource).filter(Resource.name == ent.text).scalar()
                    resource.potential = False
                    self.session.add(resource)
        self.session.commit()
