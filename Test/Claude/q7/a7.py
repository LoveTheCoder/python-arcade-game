class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def delete_node(head, position):
    if not head:  # Empty list
        return None
    
    if position == 0:  # Delete head
        return head.next
    
    current = head
    for i in range(position - 1):
        if not current:  # Position out of bounds
            return head
        current = current.next
    
    if not current or not current.next:  # Position out of bounds
        return head
    
    current.next = current.next.next
    return head

def insert(head, data):
    new_node = Node(data)
    if not head:
        return new_node
    
    current = head
    while current.next:
        current = current.next
    current.next = new_node
    return head

def print_list(head):
    current = head
    while current:
        print(current.data, end=" -> ")
        current = current.next
    print("None")

def main():
    # Test cases
    head = None
    values = [1, 2, 3, 4, 5]
    
    # Create list
    for value in values:
        head = insert(head, value)
    
    print("Original list:")
    print_list(head)
    
    # Test deletions
    positions = [0, 2, 4]  # Delete head, middle, and tail
    for pos in positions:
        head = delete_node(head, pos)
        print(f"\nAfter deleting position {pos}:")
        print_list(head)

if __name__ == "__main__":
    main()