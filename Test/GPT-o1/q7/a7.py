class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def delete_node(head, position):
    if position == 0:
        return head.next
    current = head
    for _ in range(position - 1):
        if not current or not current.next:
            return head
        current = current.next
    if current.next:
        current.next = current.next.next
    return head

if __name__ == "__main__":
    n = int(input().strip())
    values = list(map(int, input().split()))
    pos = int(input().strip())
    
    head = Node(values[0])
    current = head
    for v in values[1:]:
        current.next = Node(v)
        current = current.next
    
    head = delete_node(head, pos)
    while head:
        print(head.data, end=' ')
        head = head.next