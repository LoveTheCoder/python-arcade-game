#include <iostream>

struct Node {
    int data;
    Node* next;
    Node(int d) : data(d), next(nullptr) {}
};

Node* insertAtTail(Node* head, int data) {
    Node* newNode = new Node(data);
    
    if (head == nullptr) {
        return newNode;
    }
    
    Node* current = head;
    while (current->next != nullptr) {
        current = current->next;
    }
    current->next = newNode;
    return head;
}

void printList(Node* head) {
    Node* current = head;
    while (current != nullptr) {
        std::cout << current->data << " -> ";
        current = current->next;
    }
    std::cout << "nullptr" << std::endl;
}

void cleanup(Node* head) {
    while (head != nullptr) {
        Node* temp = head;
        head = head->next;
        delete temp;
    }
}

int main() {
    Node* head = nullptr;
    int test_data[] = {5, 10, 15, 20, 25};
    
    for (int data : test_data) {
        head = insertAtTail(head, data);
        std::cout << "After inserting " << data << ":" << std::endl;
        printList(head);
    }
    
    cleanup(head);
    return 0;
}