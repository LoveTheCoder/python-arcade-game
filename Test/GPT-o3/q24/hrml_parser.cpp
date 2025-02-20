#include <iostream>
#include <sstream>
#include <map>
#include <stack>
using namespace std;

int main() {
    int N, Q;
    cin >> N >> Q;
    cin.ignore(); // consume newline

    map<string, string> attrMap;
    stack<string> tagStack;

    for (int i = 0; i < N; i++) {
        string line;
        getline(cin, line);
        
        // Check if it's a closing tag
        if (line.substr(0, 2) == "</") {
            tagStack.pop();
        } else {
            // Remove '<' and '>' from the line
            string content = line.substr(1, line.size() - 2);
            stringstream ss(content);
            string tagName;
            ss >> tagName;

            // Build the full path for current tag
            string currPath = tagStack.empty() ? tagName : tagStack.top() + "." + tagName;
            tagStack.push(currPath);
            
            // Process attribute-value pairs
            string attrName, eq, attrValue;
            while (ss >> attrName) {
                ss >> eq >> attrValue; // attrValue will include quotes
                // Remove the surrounding quotes from attrValue
                attrValue = attrValue.substr(1, attrValue.size()-2);
                // Construct the key: full tag path + "~" + attribute name
                string key = currPath + "~" + attrName;
                attrMap[key] = attrValue;
            }
        }
    }
    
    for (int i = 0; i < Q; i++) {
        string query;
        getline(cin, query);
        if (attrMap.find(query) != attrMap.end())
            cout << attrMap[query] << endl;
        else
            cout << "Not Found!" << endl;
    }
    
    return 0;
}