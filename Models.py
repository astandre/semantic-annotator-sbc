from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists

Base = declarative_base()


# association_table = Table('sentence_word', Base.metadata,
#                           Column('sentence_id', Integer, ForeignKey('sentence.id')),
#                           Column('word_id', Integer, ForeignKey('word.id'))
#                           )

class Context(Base):
    __tablename__ = 'context'

    id = Column(Integer, primary_key=True)
    context = Column(String(300), nullable=False)
    resource = relationship("Resource", back_populates="context")
    sentence = relationship("Sentence", back_populates="context")

    def __repr__(self):
        return "<Context(context='%s')>" % self.context

    @staticmethod
    def check_context(session, context):
        return session.query(exists().where(Context.context == context)).scalar()


class Resource(Base):
    __tablename__ = 'resource'

    id = Column(Integer, primary_key=True)
    name = Column(String(300), nullable=False)
    # pos = Column(String(10), nullable=True)
    type = Column(String(10), nullable=True)
    # TODO set dicctionario for type
    resource = Column(String(300), nullable=True)
    context_id = Column(Integer, ForeignKey('context.id'))
    context = relationship("Context", back_populates="resource")

    def __repr__(self):
        return "<Resource(resource='%s')>" % self.name

    @staticmethod
    def check_resource(session, name, ct_id):
        return session.query(exists().where(Resource.name == name).where(Resource.context_id == ct_id)).scalar()


class Sentence(Base):
    __tablename__ = 'sentence'

    id = Column(Integer, primary_key=True)
    sentence = Column(String(300), nullable=False)
    word = relationship("Word", back_populates="sentence")
    context_id = Column(Integer, ForeignKey('context.id'))
    context = relationship("Context", back_populates="sentence")

    def __repr__(self):
        return "<Sentence(sentence='%s')>" % self.sentence

    __mapper_args__ = {
        'polymorphic_identity': 'sentence',
    }


class Word(Base):
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True)
    word = Column(String(100), nullable=False)
    lemma = Column(String(100), nullable=False)
    # lemma = Column(Integer, ForeignKey('word.id'), nullable=True)
    pos = Column(String(10), nullable=False)
    order = Column(Integer, nullable=False)
    # synonym = Column(Integer, ForeignKey('word.id'), nullable=True)
    sentence_id = Column(Integer, ForeignKey('sentence.id'))
    sentence = relationship("Sentence", back_populates="word")

    # sentence = relationship(
    #     "Sentence",
    #     secondary=association_table,
    #     back_populates="word")

    def __repr__(self):
        return "<Word(word='%s', pos='%s')>" % (
            self.word, self.pos)

    @staticmethod
    def check_word(session, word):
        return session.query(exists().where(Word.word == word)).scalar()

    __mapper_args__ = {
        'polymorphic_identity': 'word',
    }
