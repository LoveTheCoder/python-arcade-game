#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <sstream>

class Tag {
public:
    std::string name;
    std::map<std::string, std::string> attributes;
    std::vector<Tag*> children;
    Tag* parent;
    
    Tag(std::string n, Tag* p = nullptr) : name(n), parent(p) {}
};

std::string processQuery(Tag* root, std::string query) {
    std::stringstream ss(query);
    std::string token, attrName;
    Tag* current = root;
    
    while (getline(ss, token, '.')) {
        size_t tilde = token.find('~');
        if (tilde != std::string::npos) {
            std::string tagName = token.substr(0, tilde);
            attrName = token.substr(tilde + 1);
            token = tagName;
        }
        
        bool found = false;
        for (Tag* child : current->children) {
            if (child->name == token) {
                current = child;
                found = true;
                break;
            }
        }
        
        if (!found) return "Not Found!";
    }
    
    auto it = current->attributes.find(attrName);
    if (it != current->attributes.end())
        return it->second;
    return "Not Found!";
}

int main() {
    int n, q;
    std::cin >> n >> q;
    std::cin.ignore();
    
    Tag* root = new Tag("root");
    Tag* current = root;
    
    // Parse HRML
    for (int i = 0; i < n; i++) {
        std::string line;
        getline(std::cin, line);
        
        if (line[1] == '/') {
            current = current->parent;
            continue;
        }
        
        std::stringstream ss(line);
        std::string token;
        ss >> token;  // Get tag name
        
        std::string tagName = token.substr(1);
        Tag* newTag = new Tag(tagName, current);
        current->children.push_back(newTag);
        
        // Parse attributes
        while (ss >> token) {
            if (token == "=") {
                std::string attrName = ss.str();
                ss >> token;  // Get value
                newTag->attributes[attrName] = token.substr(1, token.length()-2);
            }
        }
        
        current = newTag;
    }
    
    // Process queries
    for (int i = 0; i < q; i++) {
        std::string query;
        getline(std::cin, query);
        std::cout << processQuery(root, query) << std::endl;
    }
    
    return 0;
}