#include <iostream>
#include <string>
using namespace std;


class Quadrilateral {
  public: 
    void properties() {
      cout << "Quadrilateral: sides are " << SideProperties() <<" and angles are " << AnglesProperties() << endl;
    }
  string SideProperties() {return "ordinary";}
  string AnglesProperties() {return "ordinary";}
};
