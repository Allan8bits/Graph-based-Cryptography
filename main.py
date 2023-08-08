###########################################################
# Nome do projeto: Criptografia baseada em Grafos
# Autor: Allan Rodrigo
# Data: 15/06/2023
###########################################################

import random
import networkx as nx
import matplotlib.pyplot as plt

class GraphCipher:
    GRAPH_SIZE = 256

    def __init__(self):
        self.graph = {}
        self.scrambled_graph = {}

    def generate_graph(self):
        # Generate the original graph with sequential edges
        self.graph = {chr(i): [chr((i + 1) % self.GRAPH_SIZE)] for i in range(self.GRAPH_SIZE)}

    def scramble_graph(self):
        # Shuffle the graph
        keys = list(self.graph.keys())
        random.shuffle(keys)

        # Update the edges with shuffled keys
        self.scrambled_graph = {}
        for i, key in enumerate(keys):
            next_key = keys[(i + 1) % len(keys)]
            self.scrambled_graph[key] = [next_key]

    def encode_message(self, message: str) -> str:
        # Encode the message using the scrambled graph
        encoded_message = []
        encoding_path = []
        encoding_keys = []
        for char in message:
            if char in self.scrambled_graph:
                encoded_char = random.choice(self.scrambled_graph[char])
                encoded_message.append(encoded_char)
                encoded_message.append(self.scrambled_graph[encoded_char][0])
                encoding_path.extend([char, encoded_char])
                encoding_keys.extend([char, encoded_char, self.scrambled_graph[char][0]])
            else:
                encoded_message.append(char)
        return "".join(encoded_message), encoding_path, encoding_keys

    def decode_message(self, encoded_message: str) -> str:
        # Decode the message using the scrambled graph
        reverse_graph = {value[0]: key for key, values in self.scrambled_graph.items() for value in values}
        decoded_message = []
        decoding_path = []
        i = 0
        while i < len(encoded_message):
            char = encoded_message[i]
            if char in reverse_graph:
                decoded_message.append(reverse_graph[char])
                decoding_path.extend([char, reverse_graph[char]])
                i += 1
            else:
                decoded_message.append(char)
            i += 1
        return "".join(decoded_message), decoding_path

    def visualize_graph(self, graph):
        # Visualize the graph using networkx and matplotlib
        G = nx.DiGraph()

        for char, edges in graph.items():
            G.add_node(char)
            for edge in edges:
                G.add_edge(char, edge)

        pos = nx.spring_layout(G, seed=42, k=0.7)
        node_colors = ['lightgreen'] * len(G.nodes())
        edge_colors = ['black'] * len(G.edges())

        plt.figure(figsize=(10, 6))
        nx.draw_networkx(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=800,
                         font_size=10, font_weight='bold', arrows=True, arrowsize=15, arrowstyle='->', linewidths=1,
                         alpha=0.8)

        plt.title("Graph Visualization", fontsize=16)
        plt.xticks([])
        plt.yticks([])
        plt.tight_layout()
        plt.show()

    def visualize_path(self, path):
        # Visualize the path using networkx and matplotlib
        G = nx.DiGraph()

        for i in range(0, len(path), 2):
            G.add_edge(path[i], path[i+1])

        pos = nx.spring_layout(G, seed=42, k=0.3)
        node_colors = ['lightblue'] * len(G.nodes())
        edge_colors = ['red'] * len(G.edges())

        plt.figure(figsize=(10, 6))
        nx.draw_networkx(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=800,
                         font_size=10, font_weight='bold', arrows=True, arrowsize=15, arrowstyle='->', linewidths=1,
                         alpha=0.8)

        plt.title("Path Visualization", fontsize=16)
        plt.xticks([])
        plt.yticks([])
        plt.tight_layout()
        plt.show()

def run_cipher():
    cipher = GraphCipher()

    # Generate the original graph
    cipher.generate_graph()
    print("Original Graph:")
    cipher.visualize_graph(cipher.graph)
    print()

    # Shuffle the graph
    cipher.scramble_graph()
    print("Scrambled Graph:")
    cipher.visualize_graph(cipher.scrambled_graph)
    print()

    # Get the message from the user
    message = input("Enter a message: ")

    # Encode the message
    encoded_message, encoding_path, encoding_keys = cipher.encode_message(message)
    print("Encoded Message:", encoded_message)
    print("Encoding Path:")
    cipher.visualize_path(encoding_path)
    print("Encoding Keys:", encoding_keys)
    print()

    # Decode the message
    decoded_message, decoding_path = cipher.decode_message(encoded_message)
    print("Decoded Message:", decoded_message)
    print("Decoding Path:")
    cipher.visualize_path(decoding_path)
    
    # Final prints for validation
    print("\n\n__________________________________________________\n")
    print("Original Message:", message)
    print("Encoded Message:", encoded_message)
    print("Decoded Message:", decoded_message)
    print("__________________________________________________")

if __name__ == "__main__":
    run_cipher()