class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def insert_node_at_tail(head, data):
    new_node = Node(data)
    if head is None:
        return new_node
    current = head
    while current.next:
        current = current.next
    current.next = new_node
    return head

if __name__ == "__main__":
    n = int(input().strip())
    values = list(map(int, input().split()))
    val_to_add = int(input().strip())
    
    head = None
    for v in values:
        head = insert_node_at_tail(head, v)
    head = insert_node_at_tail(head, val_to_add)
    
    while head:
        print(head.data, end=' ')
        head = head.next