class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def insert_into_bst(root, val):
    if not root:
        return Node(val)
    if val < root.data:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)
    return root

def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        print(root.data, end=' ')
        inorder_traversal(root.right)

if __name__ == "__main__":
    n = int(input("Enter number of values to insert: ").strip())
    values = list(map(int, input("Enter the values: ").split()))
    root = None
    for v in values:
        root = insert_into_bst(root, v)
    
    print("Inorder traversal of the BST:")
    inorder_traversal(root)
    print()