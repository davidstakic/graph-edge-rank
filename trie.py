class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.counter = 0
        self.status_ids = []
        self.children = {}

class Trie:
    def __init__(self):
        self.root = TrieNode("")
        self.output = []

    def insert(self, word, status_id):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
        node.is_end = True
        node.counter += 1
        node.status_ids.append(status_id)

    def dfs(self, node, prefix):
        if node.is_end:
            self.output.append((prefix + node.char, node.counter, node.status_ids))
        for child in node.children.values():
            self.dfs(child, prefix + node.char)

    def query(self, x):
        self.output = []
        node = self.root
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        self.dfs(node, x[:-1])
        return sorted(self.output, key=lambda x: x[1], reverse=True)
