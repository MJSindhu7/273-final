import hashlib
from dataclasses import dataclass


class Node(object):
    def __init__(self, val=None, left=None, right=None):
        # Hash value of the node via hashlib.sha256(xxxxxx.encode()).hexdigest()
        self.val = val
        # Left node
        self.left = left
        # Right node
        self.right = right

    def __str__(self):
        return f':val={self.val},left={self.left},right={self.right}:'


class MerkleTrees(object):
    def __init__(self):
        self.root = None
        # txns dict: { hash_val -> 'file_path' }
        self.txns = None

    def get_root_hash(self):
        return self.root.val if self.root else None

    def build(self, txns):
        """
        Construct a Merkle tree using the ordered txns from a given txns dictionary.
        """
        # save the original txns(files) dict while building a Merkle tree.
        self.txns = txns
        txns_list = list(txns.keys())
        if len(txns_list) % 2 != 0:
            txns_list.append(txns_list[-1])
        nonleaf_nodes = []
        for index in range(0, len(txns_list) - 1, 2):
            left = txns_list[index]
            right = txns_list[index + 1]
            combine = left + right
            root = hashlib.sha256(combine.encode()).hexdigest()
            current_node = Node(root, Node(left), Node(right))
            nonleaf_nodes.append(current_node)
            # TODO
        for index in range(0, len(nonleaf_nodes) - 1, 2):
            left = nonleaf_nodes[index]
            right = nonleaf_nodes[index + 1]
            combine = left.val + right.val
            root = hashlib.sha256(combine.encode()).hexdigest()
            current_node = Node(root, left, right)
        self.root = current_node

    def print_level_order(self):
        """
          1             1
         / \     -> --------------------    
        2   3       2 3
        """
        # TODO

        print(self.root.val)
        print("--------------------")
        left = self.root.left
        right = self.root.right
        print(f"{left.val} {right.val}")
        print("--------------------")
        left1 = left.left.val
        right2 = left.right.val

        left3 = right.left.val
        right4 = right.right.val
        print(f"{left1} {right2} {left3} {right4}")
        print("--------------------")

    @staticmethod
    def compare(x, y):
        """
        Compare a given two merkle trees x and y.
        x: A Merkle Tree
        y: A Merkle Tree
        Pre-conditions: You can assume that number of nodes and heights of the given trees are equal.
        
        Return: A list of pairs as Python tuple type(xxxxx, yyyy) that hashes are not match.
        https://realpython.com/python-lists-tuples/#python-tuples
        """
        diff = []
        if x.get_root_hash() == y.get_root_hash():
            return diff

        def check_nodes(node1, node2):
            if not (node1 and node2):
                return
            if node1.val != node2.val:
                diff.append((node1.val, node2.val))
            check_nodes(node1.left, node2.left)
            check_nodes(node1.right, node2.right)

        check_nodes(x.root, y.root)
        return diff
