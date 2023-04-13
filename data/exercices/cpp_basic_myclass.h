#include <iostream>
using namespace std;

// Declare a new class
class MyClass {
  // Set all members of the class as public
  // All members should be declared in the class declaration
  private:
    void getFirstName();
    int myNum;        // Attribute (int variable)
    string myString;  // Attribute (string variable)

  public:
    MyClass(int yourNum) {myNum = yourNum;}
    MyClass(string yourString);
    MyClass(string yourString, int yourNum);
    MyClass() {cout << "Je fais rien" << endl;}

    void getLastName() {cout <<"Doe" << endl;}
    void getFirstName2() {getFirstName();}

    void setMyNum(int yourNum) {myNum = yourNum;}
    int getMyNum() {return myNum;}
};
