class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def print_linked_list(head):
    current = head
    while current:
        print(current.data)
        current = current.next

if __name__ == "__main__":
    n = int(input().strip())
    if n == 0:
        # No elements to print
        exit(0)
    values = list(map(int, input().split()))
    head = Node(values[0])
    current = head
    for item in values[1:]:
        current.next = Node(item)
        current = current.next
    print_linked_list(head)