#include "myclass.h"

// Function can be implemented from outside the declaration
void MyClass::getFirstName(){
    cout << "John" << endl;
}

MyClass::MyClass(string yourString) {
    myString = yourString;
    }
MyClass::MyClass(string yourString, int yourNum) {
    myString = yourString;
        myNum = yourNum;
    }
