import matplotlib.pyplot as plt
from Models import *
import networkx as nx
import csv


class Graph:
    nodes = None
    edges = None
    G = nx.Graph()

    def __init__(self, nlp, context_id, session):
        self.nlp = nlp
        self.context_id = context_id
        self.session = session
        self.create_graph()

    def decompose_sentence_to_graph(self, ):
        nodes = []
        edges = []
        sentences = self.session.query(Sentence).filter(Sentence.context_id == self.context_id)
        last_word = ""
        for sentence in sentences:
            print(sentence.sentence)
            cont = 0
            for word in self.session.query(Word).filter(Word.sentence_id == sentence.id,
                                                        (~Word.pos.in_(['ADP', 'AUX', 'CONJ']))):

                exists = False
                print(">>>>>>", word.lemma, word.pos)
                # Setting up edges

                if cont >= 1:
                    edges.append([last_word, word.lemma])
                cont += 1
                last_word = word.lemma
                # Checking if word exists in nodes list
                for node in nodes:
                    if word.lemma == node:
                        exists = True
                        break
                #         Adding word to nodes list
                if not exists:
                    nodes.append(word.lemma)
        return nodes, edges, sentences

    def create_graph(self):
        nodes, edges, sentences = self.decompose_sentence_to_graph()

        # Generating graph

        self.G.add_nodes_from(nodes)
        self.G.add_edges_from(edges)

    def get_graph_centraility(self):
        # Getting degree of nodes
        degrees = [self.G.degree(node) for node in self.nodes]
        print(degrees)
        max_degree = max(degrees)
        min_degree = min(degrees)
        umbral = 0.4 * max_degree
        new_nodes = [self.nodes[i] for i, degree in enumerate(degrees) if degree > umbral]
        print(new_nodes)
        for node in new_nodes:
            if not Resource.check_resource(self.session, node, self.context_id):
                print("Resource %s not found!" % node)
                resource = Resource(name=node, type="W", context_id=self.context_id)
                self.session.add(resource)
            else:
                print("Resource  %s found!" % node)
        self.session.commit()

        return self.session.query(Resource).filter(Resource.context_id == self.context_id)

    def draw(self):
        # nx.draw_planar(self.G, with_labels=True, font_weight='bold')
        # nx.draw_circular(self.G, with_labels=True, font_weight='bold')
        # nx.draw_kamada_kawai(self.G, with_labels=True, font_weight='bold')
        # nx.draw_spectral(self.G, with_labels=True, font_weight='bold')
        nx.draw_random(self.G, with_labels=True, font_weight='bold')
        # nx.draw_spring(self.G, with_labels=True, font_weight='bold')
        # nx.draw_shell(self.G, with_labels=True, font_weight='bold')

        plt.show()

    def save(self):
        # nx.draw_circular(self.G, with_labels=True, font_weight='bold')
        nx.draw_kamada_kawai(self.G, with_labels=True, font_weight='bold')
        plt.savefig("image.png")

    def export(self):
        with open('words.csv', mode='w') as csv_file:
            fieldnames = ['source', 'target']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for edge in self.edges:
                writer.writerow({'source': edge[0], 'target': edge[1]})
