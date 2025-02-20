class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

def insertAtTail(head, data):
    new_node = ListNode(data)
    if head is None:
        return new_node
    current = head
    while current.next:
        current = current.next
    current.next = new_node
    return head

# Helper function to print linked list
def print_list(head):
    current = head
    result = []
    while current:
        result.append(str(current.data))
        current = current.next
    print(" -> ".join(result))

if __name__ == '__main__':
    # Create an initial linked list from input
    values = list(map(int, input("Enter space separated values for the linked list (or leave empty): ").split()))
    head = None
    for value in values:
        head = insertAtTail(head, value)
    
    # Insert new node at the tail
    new_data = int(input("Enter the integer to add at the tail: "))
    head = insertAtTail(head, new_data)
    
    print("Updated linked list:")
    print_list(head)