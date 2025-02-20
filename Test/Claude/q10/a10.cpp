#include <iostream>

struct Node {
    int data;
    Node* next;
    Node(int d) : data(d), next(nullptr) {}
};

int has_cycle(Node* head) {
    if (head == nullptr || head->next == nullptr) {
        return 0;
    }
    
    Node* slow = head;
    Node* fast = head;
    
    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
        
        if (slow == fast) {
            return 1;
        }
    }
    
    return 0;
}

// Test helper functions
Node* create_test_list(bool create_cycle) {
    Node* head = new Node(1);
    Node* second = new Node(2);
    Node* third = new Node(3);
    Node* fourth = new Node(4);
    
    head->next = second;
    second->next = third;
    third->next = fourth;
    
    if (create_cycle) {
        fourth->next = second;  // Create cycle
    }
    
    return head;
}

void cleanup(Node* head, bool has_cycle) {
    if (has_cycle || head == nullptr) {
        return;  // Avoid infinite loop in cleanup
    }
    
    while (head != nullptr) {
        Node* temp = head;
        head = head->next;
        delete temp;
    }
}

int main() {
    // Test 1: No cycle
    Node* list1 = create_test_list(false);
    std::cout << "List without cycle: " << has_cycle(list1) << std::endl;
    cleanup(list1, false);
    
    // Test 2: With cycle
    Node* list2 = create_test_list(true);
    std::cout << "List with cycle: " << has_cycle(list2) << std::endl;
    
    // Test 3: Empty list
    std::cout << "Empty list: " << has_cycle(nullptr) << std::endl;
    
    return 0;
}