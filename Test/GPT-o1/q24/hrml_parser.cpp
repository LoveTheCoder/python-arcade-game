#include <iostream>
#include <sstream>
#include <string>
#include <stack>
#include <unordered_map>
#include <limits>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, Q;
    cin >> N >> Q;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    // We’ll keep a stack of tag names to track nesting.
    // Then we'll store attributes in a map:
    // Key: "tag1.tag2...tagN~attributeName" => value
    stack<string> tagStack;
    unordered_map<string, string> attributes;

    for(int i = 0; i < N; i++){
        string line;
        getline(cin, line);
        // Remove leading/trailing spaces if any
        // We'll parse the line to get tag name, attributes or closing tag

        // If it's a closing tag:  </tagName>
        if(line.substr(0, 2) == "</"){
            // Pop
            tagStack.pop();
        } 
        else {
            // It's an opening tag: <tagName attr1 = "val" attr2 = "val2" ...>
            // Remove '<' at start and '>' at end
            line = line.substr(1, line.size() - 2);

            // Split on spaces to get first token as tagName, then attributes
            // But watch out for '=' and quotes
            // We'll break it manually
            // First token: tagName
            stringstream ss(line);
            string tagName;
            ss >> tagName;

            // Now we add this tag name to the stack
            if(!tagStack.empty()){
                tagName = tagStack.top() + "." + tagName;
            }
            tagStack.push(tagName);

            // Now parse attributes if any
            while(ss) {
                string attrName;
                ss >> attrName;
                if(attrName.size() == 0) break;
                // attrName should be something like attribute1-name
                // Then we should see '='
                // Then the attribute value in quotes
                if(attrName == "=") continue; // unlikely but let's be safe

                // The next token is '='
                // Then the next token is the quoted string
                string eq, val;
                ss >> eq;
                ss >> val; // something like "value"
                // strip the quotes from val
                if(val.size() >= 2 && val.front() == '\"' && val.back() == '\"'){
                    val = val.substr(1, val.size() - 2);
                }
                // Build key: currentTag~attrName
                string key = tagName + "~" + attrName;
                attributes[key] = val;
            }
        }
    }

    // Now process Q queries
    for(int i = 0; i < Q; i++){
        string query;
        getline(cin, query);
        if(attributes.find(query) != attributes.end()){
            cout << attributes[query] << "\n";
        } else {
            cout << "Not Found!" << "\n";
        }
    }
    return 0;
}