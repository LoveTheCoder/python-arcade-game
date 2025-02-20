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

def inorder(root):
    if root:
        inorder(root.left)
        print(root.data, end=' ')
        inorder(root.right)

def main():
    # Test cases
    values = [4, 2, 7, 1, 3, 6, 9]
    root = None
    
    print("Inserting values:", values)
    for value in values:
        root = insert(root, value)
    
    print("\nInorder traversal of the constructed tree:")
    inorder(root)
    print()

if __name__ == "__main__":
    main()