import matplotlib.pyplot as plt

class Node:
    def __init__(self, start, end, suffix_link=None):
        self.start = start
        self.end = end
        self.suffix_link = suffix_link
        self.children = {}

class SuffixTree:
    def __init__(self, text):
        self.root = Node(-1, -1)
        self.root.suffix_link = self.root
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        self.remaining_suffix_count = 0
        self.text = text
        self.end = -1  # Represents the last internal node created
        self.build_suffix_tree()

    def build_suffix_tree(self):
        n = len(self.text)
        for i in range(n):
            self.remaining_suffix_count += 1
            self.end += 1
            self.extend_suffix_tree(i)

    def extend_suffix_tree(self, i):
        global root
        self.remaining_suffix_count += 1
        last_created_internal_node = None
        self.root.suffix_link = self.root

        while self.remaining_suffix_count > 0:
            if self.active_length == 0:
                self.active_edge = i

            if self.text[i] not in self.active_node.children:
                leaf = Node(i, len(self.text))
                self.active_node.children[self.text[i]] = leaf

                if last_created_internal_node is not None:
                    last_created_internal_node.suffix_link = self.active_node
                    last_created_internal_node = None
            else:
                next_node = self.active_node.children[self.text[i]]
                edge_length = min(next_node.end, i + 1) - next_node.start

                if self.active_length >= edge_length:
                    self.active_edge += edge_length
                    self.active_length -= edge_length
                    self.active_node = next_node
                    continue

                if self.text[next_node.start + self.active_length] == self.text[i]:
                    self.active_length += 1

                    if last_created_internal_node is not None and self.active_node != self.root:
                        last_created_internal_node.suffix_link = self.active_node
                        last_created_internal_node = None

                    break

                # Split the edge
                new_internal_node = Node(next_node.start, next_node.start + self.active_length, suffix_link=self.root)
                new_internal_node.children[self.text[i]] = Node(i, len(self.text))
                next_node.start += self.active_length
                new_internal_node.children[self.text[next_node.start]] = next_node
                self.active_node.children[self.text[i]] = new_internal_node

                if last_created_internal_node is not None:
                    last_created_internal_node.suffix_link = new_internal_node

                last_created_internal_node = new_internal_node

            self.remaining_suffix_count -= 1

            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = i - self.remaining_suffix_count + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link

    def draw_suffix_tree(self, node, x, y, dx, ax):
        for child in node.children.values():
            ax.plot([x, child.start], [y, -child.end], color='black', linestyle='-', linewidth=1, markersize=8)
            label = self.text[child.start:child.end]
            ax.text(child.start, -child.end, label, ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=0.3'))
            self.draw_suffix_tree(child, child.start, -child.end, dx * 0.5, ax)

    def visualize_suffix_tree(self):
        fig, ax = plt.subplots()
        self.draw_suffix_tree(self.root, 0, 0, 10, ax)
        ax.set_aspect('equal')
        ax.set_xlabel('Suffix Tree')
        ax.set_title('Visualization of Suffix Tree')
        plt.show()

# Example usage
print("Enter a word to visualise the suffix tree construction")
text=input()
tree = SuffixTree(text)
tree.visualize_suffix_tree()
