#include "myclass.h"

int main() {
  MyClass myObj;  
  myObj.setMyNum(70);
  cout << myObj.getMyNum() <<endl;
  return 0;

  // Create object from MyClass
  MyClass myObj3;  
  MyClass myObj2("youpi");  

  // Access attributes and set values
  myObj.setMyNum(70);
  cout << myObj.getMyNum() <<endl;

  myObj.setMyNum(35);
  cout << myObj.getMyNum() <<endl;

  //myObj.myString = "yop";

  // Print values
  myObj.getFirstName2();
  myObj.getLastName();
  cout << myObj.getMyNum() <<endl;
  //cout << myObj.myString <<endl; 
  return 0;
}
