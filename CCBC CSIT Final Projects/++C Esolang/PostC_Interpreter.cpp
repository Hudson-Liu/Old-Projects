/*                            
                          ,ad8888ba,   
    aa          aa       d8"'    `"8b  
    88          88      d8'            
aaaa88aaaa  aaaa88aaaa  88             
""""88""""  """"88""""  88             
    88          88      Y8,            
    ""          ""       Y8a.    .a8P  
                          `"Y8888Y"'   
                                       */
// ++C (AKA PostC)
// A basic Postfix Scripting Language Lexer + Interpreter
// By Hudson Liu

#include <iostream>
#include <stack>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <map>

using namespace std;

class Interpreter{
    public:
        //Constructors
        Interpreter();
        Interpreter(string fileContents);

        //Remove comments
        void removeComments();

        //Parses the string into a set of identifiers
        void parseFile();

        //Main loop, loops through each line of file and translates + runs each line
        void identifierIterator();
    private:
        string fileContents;
        vector<string> parsed;

        vector<int> integerVars; //i
        vector<string> stringVars; //s
        vector<bool> boolVars; //b

        stack<string> operands;
        map<string, pair<char, int>> variableKey; /// string is variable name, char is datatype, int is index

        //A bunch of switch cases that determines what function the identifier should be handled by
        void identifierHandoff(string identifier);

        //Detects whether an identifier is a variable or not
        bool isVariableName(string identifier);

        //Access variable by identifier, and return the proper type; throws error if variable is not correct type 
        int getInt(string variableName);
        string getString(string variableName);
        bool getBool(string variableName);

        //Quick conversion from char abbreviation to full datatype name, used for getInt, getString, and getBool error messages
        string charToDatatype(char datatype);

        ///IMPORTANT NOTE: Handlers only exist for operator, all operands are added equally to the operand list

        //If a "string" variable declaration is detected, the last operand will be added to the variableKey list as a string 
        void stringDeclarationHandler();

        //If an "int" variable declaration is detected, the last operand will be added to the variableKey list as an int
        void intDeclarationHandler();

        //If a "bool" variable declaration is detected, the last operand will be added to the variableKey list as a bool
        void boolDeclarationHandler();

        //If a stream insertion operator << is detected, the second-to-last operand on the stack will be inserted into the last operand 
        void streamInsertionHandler();

        //If a stream extraction operator >> is detected, the second-to-last operand on the stack will be given the input of the last operand
        void streamExtractionHandler();

        //If an addition operator is detected, perform addition (obviously)
        void additionHandler();

        //If a subtraction operator is detected, perform subtraction (you wouldn't say)
        void subtractionHandler();

        //If a multiplication operator is detected, perform multiplication (was this code written by a toddler?)
        void multiplicationHandler();

        //If a division operator is detected, perform division
        void divisionHandler();
};

int main(){

    //Open file
    string filename;
    cout << "Name of file: ";
    cin >> filename;
    ifstream fin;
    fin.open(filename);
    if (fin.fail()){
        cout << "Input file opening failed";
        exit(1);
    }

    //Get all lines and store it in a big string
    string program;
    while(!fin.eof()){
        char character = fin.get();
        if (character != '\n'){
            program = program + character;
        }
    }
    cout << program;

    //Runs the Interpreter
    Interpreter interpret(program);
    interpret.parseFile();
    interpret.identifierIterator();

    return 0;
}

Interpreter::Interpreter(){
    cout << "invalid Argument to Interpreter Class; constructor arguments must not be empty" << endl;
    exit(1);
}

Interpreter::Interpreter(string fileContents){
    Interpreter::fileContents = fileContents;
}

void Interpreter::removeComments(){
    //Loops until the end of the program
    int cursor = 1;
    int size = 1;
    char currentChar = ' ';
    char prevChar = 'L'; //Placeholder character; it just needs to not be '/', ' ', or '\"'
    bool commentClearance = false;
    string cleaned;
    while (cursor < fileContents.length()){
        //Updates currentChar
        currentChar = fileContents[cursor];
        prevChar = fileContents[cursor - 1];

        //Detect comments
        if (currentChar != '/' || prevChar != '/'){
            cleaned += prevChar;
            cursor++;
        }
        else{
            //Clear cursor from any additional /'s attached to the string
            cursor++;
            //Move past comment
            do{
                cursor++;
                currentChar = fileContents[cursor];
                prevChar = fileContents[cursor - 1];
            } while(currentChar != '/' || prevChar != '/');
            //Clear the two end //'ss
            cursor+=2;
        }
    }
    //Gets last character only if the last characters weren't a comment
    if (cursor == fileContents.length() + 1){
        currentChar = fileContents[cursor];
        cleaned += currentChar;
    }
    fileContents = cleaned;
}

void Interpreter::parseFile(){
    //Removes Comments
    removeComments();
    
    //Loops until the end of a statement
    int cursor = 0;
    int size = 1;
    char currentChar = ' ';
    char prevChar = 'L'; //Placeholder character; it just needs to not be '/', ' ', or '\"'
    while (cursor < fileContents.length()){
        //Updates currentChar
        currentChar = fileContents[cursor];
        if (cursor > 0){
            prevChar = fileContents[cursor - 1];
        }

        //If the current character is a quote, skip to the end of it, then make that whole quote one big identifier
        if(currentChar == '\"'){
            int starter = cursor;
            int sizeStr = 1;
            do {
                cursor++;
                sizeStr++;
                currentChar = fileContents[cursor];
            } while (currentChar != '\"');
            cursor+=2;
            string substring = fileContents.substr(starter, sizeStr);
            parsed.push_back(substring);
        }
        //If the current character is a whitespace, add the past word to the list as a substring, unless there was an accidental double space
        else if (currentChar == ' ' && prevChar != ' '){
            //Add the parsed substring to the vector, and reset size and update the cursor position
            string substring = fileContents.substr((cursor - size) + 1, size - 1);
            parsed.push_back(substring);
            size = 1;
            
            //Ensure the cursor position is past any additional spaces
            currentChar = fileContents[cursor];
            while (currentChar == ' '){
                cursor++;
                currentChar = fileContents[cursor];
            }
        }
        //If the current character is a semicolon, adds the current identifier and the semicolon to parsed, then skip past the semicolon
        else if (currentChar == ';'){
            string substring = fileContents.substr((cursor - size) + 1, size - 1);
            parsed.push_back(substring);
            string semicolon = fileContents.substr(cursor, 1);
            parsed.push_back(semicolon);
            cursor++;
            size = 1;
        }
        //If it isn't any special case, then iterate it as normal
        else{
            cursor++;
            size++;
        }
    }
    //TODO: Remove this after finished debugging
    for (string i : parsed){
        cout << i << endl;
    }
}

void Interpreter::identifierIterator(){
    //Iterates over all the identifiers in the "parsed" list
    for (string identifier : parsed){
        identifierHandoff(identifier);
    }
}

void Interpreter::identifierHandoff(string identifier){
    //Detects all operators and performs relevant operations; if not operator it will just append the value to operands
    if (identifier == "<<"){
        streamInsertionHandler();
    }
    else if (identifier == ";"){
        operands.empty();
    }
    else if (identifier == "int"){
        intDeclarationHandler();
    }
    else if (identifier == "string"){
        stringDeclarationHandler();
    }
    else if (identifier == "bool"){
        boolDeclarationHandler();
    }
    else if (identifier == ">>"){
        streamExtractionHandler();
    }
    else {
        operands.push(identifier);
    }
}
void Interpreter::streamInsertionHandler(){
    //Pull the two relevant operators off the stack
    string outputStream = operands.top();
    operands.pop();
    string text = operands.top();
    operands.pop();
    //Check for a valid rvalue
    if (outputStream == "cout"){
        //Find the appropriate action to take based off of the lvalue
        if (text[0] == '\"' && text[text.length() - 1] == '\"'){
            string noQuotes = text.substr(1, text.length() - 2);
            cout << noQuotes;
        }
        else if (isVariableName(text)){
            string returnText = getString(text);
            cout << returnText;
        }
        else if (text == "endl"){
            cout << "\n";
        }
        else{
            cout << "++C ERROR: Stream insertion operator lvalue expected string or modifier, received: \"" << text << "\"\n";
            exit(1);
        }

        // "<<" operator returns cout
        operands.push("cout");
    }
    else{
        cout << "++C ERROR: Stream insertion operator rvalue expected \"cout\", received: \"" << outputStream << "\"\n";
        exit(1);
    }
}

void Interpreter::streamExtractionHandler(){
    //Pull the two relevant operators off the stack
    string inputStream = operands.top();
    operands.pop();
    string varName = operands.top();
    operands.pop();
    //Check for a valid rvalue
    if (inputStream == "cin"){
        //Find the appropriate action to take based off of the lvalue
        if (isVariableName(varName)){
            //TODO search the key for the variable, then use the index to create a refernece to that varaible along the lines of integerVars[i] to have the cin feed into
        }
        else{
            cout << "++C ERROR: Stream extraction operator lvalue expected variable, received: \"" << varName << "\"\n";
            exit(1);
        }

        // "<<" operator returns cout
        operands.push("cout");
    }
    else{
        cout << "++C ERROR: Stream extraction operator rvalue expected \"cin\", received: \"" << inputStream << "\"\n";
        exit(1);
    }
}

//TODO implement cin and variable assignment
void Interpreter::intDeclarationHandler(){
    //Doesn't pop the stack since variable declaration returns the variable
    string varName = operands.top();
    pair<char, int> keyPair = pair<char,int>('i', stringVars.size());
    variableKey.insert({varName, keyPair});
    integerVars.push_back(0);
}

void Interpreter::stringDeclarationHandler(){
    //Doesn't pop the stack since variable declaration returns the variable
    string varName = operands.top();
    pair<char, int> keyPair = pair<char,int>('s', stringVars.size());
    variableKey.insert({varName, keyPair});
    stringVars.push_back("");
}

void Interpreter::boolDeclarationHandler(){
    //Doesn't pop the stack since variable declaration returns the variable
    string varName = operands.top();
    pair<char, int> keyPair = pair<char,int>('b', stringVars.size());
    variableKey.insert({varName, keyPair});
    boolVars.push_back(false);
}

int Interpreter::getInt(string variableName){
    pair<char, int> pairing = variableKey.at(variableName);
    char datatype = pairing.first;
    if (datatype != 'i'){
        cout << "++C ERROR: Operator expected int, received: \"" << charToDatatype(datatype) << "\"\n";
        exit(1);
    }
    int index = pairing.second;
    return integerVars[index];
}

string Interpreter::getString(string variableName){
    pair<char, int> pairing = variableKey.at(variableName);
    char datatype = pairing.first;
    if (datatype != 's'){
        cout << "++C ERROR: Operator expected string, received: \"" << charToDatatype(datatype) << "\"\n";
        exit(1);
    }
    int index = pairing.second;
    return stringVars[index];
}

bool Interpreter::getBool(string variableName){
    pair<char, int> pairing = variableKey.at(variableName);
    char datatype = pairing.first;
    if (datatype != 'b'){
        cout << "++C ERROR: Operator expected bool, received: \"" << charToDatatype(datatype) << "\"\n";
        exit(1);
    }
    int index = pairing.second;
    return integerVars[index];
}

bool Interpreter::isVariableName(string identifier){
    return variableKey.find(identifier) != variableKey.end();
}

string charToDatatype(char datatype){
    switch (datatype){
        case 'i':
            return "int";
        case 's':
            return "string";
        case 'b':
            return "bool";
    }
}
