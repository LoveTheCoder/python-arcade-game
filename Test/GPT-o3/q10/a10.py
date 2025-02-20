class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

def hasCycle(head):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return 1
    return 0

if __name__ == '__main__':
    # Build linked list from input.
    # First, input the number of nodes.
    n = int(input("Enter the number of nodes: "))
    if n > 0:
        values = list(map(int, input("Enter the node values (space separated): ").split()))
        if len(values) != n:
            print("Error: Number of values does not match number of nodes")
            exit(1)
    else:
        values = []
    
    head = None
    nodes = []
    for val in values:
        node = ListNode(val)
        nodes.append(node)
        if head is None:
            head = node
        else:
            nodes[-2].next = node

    # Optionally create a cycle.
    # Input an integer representing the zero-indexed position that the tail should link to.
    # Enter -1 for no cycle.
    cycle_index = int(input("Enter the index for the cycle (-1 for no cycle): "))
    if cycle_index != -1:
        if 0 <= cycle_index < n:
            nodes[-1].next = nodes[cycle_index]
        else:
            print("Invalid cycle index. No cycle created.")

    print("Cycle detected:" if hasCycle(head) == 1 else "No cycle detected.")