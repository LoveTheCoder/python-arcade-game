class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

def printLinkedList(head):
    current = head
    while current:
        print(current.data)
        current = current.next

if __name__ == '__main__':
    # Create a sample linked list from input values
    values = list(map(int, input("Enter space separated values for the linked list (or leave empty): ").split()))
    head = None
    if values:
        head = ListNode(values[0])
        current = head
        for value in values[1:]:
            current.next = ListNode(value)
            current = current.next

    # Print each node's element
    printLinkedList(head)