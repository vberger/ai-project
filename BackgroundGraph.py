import pickle
from operator import itemgetter
import itertools

class BackgroundGraph:

    #constructor
    def __init__(self, nameCurrentGraph):
        #variables initialization
        self.nameCurrentGraph = nameCurrentGraph
        self.graph={}
        #Graph completion
        self.loadFileGraph()

    def addlistWords(self, listWords):
        # extract sentences
        indices = [i for i, x in enumerate(listWords) if x == "."]
        indices = [0]+indices
        listSentences = [listWords[indices[i - 1]:x] for i, x in enumerate(indices)][1:]
        # add sentences
        l = len(listSentences)
        for i,s in enumerate(listSentences):
            print(100.0*i/l)
            self.addSentence(s)

    def addSentence(self, sentence):
        for x,y in itertools.product(sentence,sentence):
            self.addWords(x,y)

    #load a graph from an existing file
    def loadFileGraph(self):
        try:
            file= open(self.nameCurrentGraph, 'rb')
            try:
                self.graph = pickle.load(file)
            except:
                print("The file doesn't contain a graph")
            file.close()
        except IOError:
            print("File couldn't be opened ! Graph will start empty")

    #save the current graph to a file        
    def saveFileGraph(self):
        file= open(self.nameCurrentGraph, 'wb')
        pickle.dump(self.graph, file)
        file.close()

    #add a new or existing combination of 2 words to the graph
    def addWords(self, word1, word2):
        w1 = (word1 in self.graph)
        w2 = word2 in self.graph
        if (word1 in self.graph) == False:
            self.graph[word1] = {}
        if (word2 in self.graph) == False:
            self.graph[word2] = {}

        if (word2 in self.graph[word1]):
            self.graph[word1][word2] += 1
        else:
            self.graph[word1][word2] = 1

        if (word1 in self.graph[word2]):
            self.graph[word2][word1] += 1
        else:
            self.graph[word2][word1] = 1

    #get the N closest neighbors        
    def getNeighbors(self, word, N):
        l=list(self.graph[word].items())
        l.sort(key=itemgetter(1),reverse=True)
        if N<len(l): return [l[i][0] for i in range(N)] 
        else:   return [l[i][0] for i in range(len(l))]

    #give the proximity between 2 words
    def prox(self, word1, word2):
        return self.graph[word1][word2]

    
"""
##########################
#CODE TESTING            #
##########################
    
#Graph creation
graph = BackgroundGraph("Test")

#Graph filling
graph.addWords("chien", "chat")
graph.addWords("souris", "chat")
graph.addWords("laisse", "chien")
graph.addWords("souris", "chat")
graph.addWords("chat", "chien")
graph.addWords("poisson", "chat")

#graph printing
print(graph.graph)

#closest neighbors
print(graph.getNeighbors("chat", 2))

#proximity between 2 words
print(graph.prox("chat", "poisson"))

#serialization
graph.saveFileGraph()

#load preexisting graph from a file
graph2 = BackgroundGraph("Test")
print(graph2.graph)
"""
            