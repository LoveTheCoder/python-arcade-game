class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def insert(root, data):
    if root is None:
        return Node(data)
    if data < root.data:
        root.left = insert(root.left, data)
    else:
        root.right = insert(root.right, data)
    return root

if __name__ == '__main__':
    # Example usage:
    # Create a BST by inserting values into it.
    values = list(map(int, input("Enter the values to insert (space separated): ").split()))
    root = None
    for val in values:
        root = insert(root, val)
    
    # Inorder traversal to verify the BST structure.
    def inorder(root):
        return inorder(root.left) + [root.data] + inorder(root.right) if root else []
    
    print("Inorder traversal of the BST:", inorder(root))