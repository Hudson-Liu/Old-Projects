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

        //Parses the string into a set of identifiers
        void parseFile();

        //Main loop, loops through each line of file and translates + runs each line
        void lineIterator();
    private:
        string fileContents;
        vector<string> program;
        vector<string> parsed;

        vector<int> integerVars; //i
        vector<string> stringVars; //s
        vector<bool> boolVars; //b

        stack<string> operands;
        map<string, pair<char, int>> variableKey; /// string is variable name, char is datatype, int is index

        //variableKey.insert()
        //pair<char, int> val = variableKey[i]
        //val.first to get first val, val.second to get second

        //A bunch of switch cases that determines what function the identifier should be handled by
        void identifierHandoff(string identifier);

        ///IMPORTANT NOTE: Handlers only exist for operator, all operands are added equally to the operand list

        //If brackets are detected {}, the line iterator will skip forward how ever many lines until the end bracket is found and resolve the expression
        void bracketHandler();

        //If quotes are detected "", the program will store it as an operand on the stack but not as a string variable
        void quoteHandler();

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

        //If an equality operator == is detected, the last two operands will be compared
        void equalityHandler();

        //If an or operator || is detected, the last two operands will be expected to be boolean values
        void orHandler();

        //If an if operator is detected, the last operand will be the conditional and the second to last operand will be the executed code
        void ifHandler();

        //If a while operator is detected, calls an instance of the line iterator on the first operand as long as the second operand (a conditional) is satisfied
        void whileLoops();
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

    return 0;
}

Interpreter::Interpreter(){
    cout << "invalid Argument to Interpreter Class; constructor arguments must not be empty" << endl;
    exit(1);
}

Interpreter::Interpreter(string fileContents){
    Interpreter::fileContents = fileContents;
}

void Interpreter::parseFile(){
    //Loops until the end of a statement
    int cursor = 0;
    int size = 1;
    char currentChar = ' ';
    char prevChar = 'L'; //Placeholder character; it just needs to not be '/', ' ', or '\"'
    bool notInRange = true;
    while (currentChar != ';'){
        //Updates currentChar
        currentChar = fileContents[cursor];
        if (cursor > 0){
            prevChar = fileContents[cursor - 1];
        }

        cout << currentChar << prevChar << endl;
        //If the current characters are a comment, move the cursor to the end of the comment
        if (currentChar == '/' && prevChar == '/'){
            //Add the current identifier to the substring since there's a comment cutting it off now
            if (size != 1){
                string substring = fileContents.substr((cursor - size) + 1, size - 1);
                parsed.push_back(substring);
                cursor += size + 1;
                size = 1;   
            }
            //Move cursor to end of comment
            do {
                cursor++;
                currentChar = fileContents[cursor];
                prevChar = fileContents[cursor - 1];
            } while (currentChar != '/' || prevChar != '/');
            cursor+=2;
        }
        //If the current character is a quote, skip to the end of it, then make that whole quote one big identifier
        else if(currentChar == '\"'){
            int starter = cursor;
            int sizeStr = 1;
            do {
                cursor++;
                sizeStr++;
                currentChar = fileContents[cursor];
            } while (currentChar != '\"');
            cursor++;
            string substring = fileContents.substr(starter, sizeStr);
            program.push_back(substring);
        }
        //If the current character is a whitespace, add the past word to the list as a substring, unless there was an accidental double space
        else if (currentChar == ' ' && prevChar != ' '){ //in case, at the start of the program, there's 
            //Add the parsed substring to the vector, and reset size and update the cursor position
            string substring = fileContents.substr((cursor - size) + 1, size);
            parsed.push_back(substring);
            cursor += size + 1;
            size = 1;
            
            //Ensure the cursor position is past any additional spaces
            currentChar = fileContents[cursor];
            while (currentChar == ' '){
                cursor++;
                currentChar = fileContents[cursor];
            }
        }
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

//some operators will neeed to be tested for character-by-character, e.g. //, ", {
void Interpreter::lineIterator(){
    
}
