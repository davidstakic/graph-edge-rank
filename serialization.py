import pickle

def load_graph():
    with open('dataset/graph.pkl', 'rb') as file:
        graph = pickle.load(file)
        return graph
    
def save_graph(graph):
    serialized_graph = pickle.dumps(graph)
    with open('dataset/graph.pkl', 'wb') as file:
        file.write(serialized_graph)

def load_trie():
    with open('dataset/trie.pkl', 'rb') as file:
        trie = pickle.load(file)
        return trie
    
def save_trie(trie):
    serialized_trie = pickle.dumps(trie)
    with open('dataset/trie.pkl', 'wb') as file:
        file.write(serialized_trie)