class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

def deleteNode(head, position):
    if head is None:
        return head
    if position == 0:
        return head.next
    current = head
    index = 0
    while current is not None and index < position - 1:
        current = current.next
        index += 1
    if current is not None and current.next is not None:
        current.next = current.next.next
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
    # Create a sample linked list
    # For example: 1 -> 2 -> 3 -> 4 -> 5
    values = list(map(int, input("Enter space separated values for the linked list: ").split()))
    if not values:
        head = None
    else:
        head = ListNode(values[0])
        current = head
        for value in values[1:]:
            current.next = ListNode(value)
            current = current.next

    position = int(input("Enter the position to delete (0-indexed): "))
    head = deleteNode(head, position)
    print("Updated linked list:")
    print_list(head)