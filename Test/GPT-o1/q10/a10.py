class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def has_cycle(head):
    if not head:
        return 0
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return 1
    return 0

if __name__ == "__main__":
    n = int(input().strip())
    # We'll build a list, but for a real test you might also create a cycle.
    values = list(map(int, input().split()))
    if n == 0:
        print(0)
        exit(0)

    head = Node(values[0])
    current = head
    nodes = [head]
    for v in values[1:]:
        new_node = Node(v)
        current.next = new_node
        current = new_node
        nodes.append(new_node)

    # Optional: Create a cycle by reading an index to which the tail should connect.
    cycle_index = int(input().strip())
    if cycle_index != -1 and 0 <= cycle_index < n:
        current.next = nodes[cycle_index]

    print(has_cycle(head))