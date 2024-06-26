import bulkhours


cell_content = """%%evaluation_cell_id -i synthetic
def generate_data(n=40):
    df["noise"] = sp.stats.norm(loc=3, scale=0.3).rvs(n) # BULKHOURS.INIT:0
    return df

for i, variable in enumerate(["noise", "trend", "seasonal", "trend+seasonal"]):
    ax = axes[i]
    # BULKHOURS.REMOVE:START
    a = 3
    # BULKHOURS.REMOVE:END

def student_evaluation_function():
    return bulkhours.is_equal(student.flops, max_score=3)

def student_hint_function():
    return yopop

def student_explanation_function():
    return tametre

# 5. Comment
print("BK ROCKS")  # BULKHOURS.REPLACE:print("...COMMENT...")
"""


def test_cell_reset_python():
    cinfo = bulkhours.core.LineParser.from_cell_id_user("synthetic", bulkhours.core.tools.REF_USER)
    teacher_data = bulkhours.core.cell_parser.CellParser.crunch_data(
        cinfo=cinfo, user=bulkhours.core.tools.REF_USER, data=cell_content
    )
    code = teacher_data.get_reset()
    print(code)

    for s in [
        "BK ROCKS",
        "student_evaluation_function",
        "student_hint_function",
        "student_explanation_function",
    ]:
        if s in code:
            raise Exception(f"Should not be here ({s})")


def test_cell_solution_python():
    cinfo = bulkhours.core.LineParser.from_cell_id_user("synthetic", bulkhours.core.tools.REF_USER)
    teacher_data = bulkhours.core.cell_parser.CellParser.crunch_data(
        cinfo=cinfo, user=bulkhours.core.tools.REF_USER, data=cell_content
    )
    code = teacher_data.get_solution()
    print(code)

    if "BULKHOURS." in code:
        raise Exception("Should not be here")

    if "...COMMENT..." in code:
        raise Exception("Should not be here")

    if "student_evaluation_function" in code:
        raise Exception("Should not be here")


cell_content_cpp = """%%evaluation_cell_id -i encapsulation
%%compile_and_exec
#include <iostream>

class MyClass {

  private:

    void getFirstName();
    int myNum;        // Attribute (int variable)

  public:
    // BULKHOURS.REMOVE:START
    MyClass(int yourNum) {myNum = yourNum;}
    void getLastName() {cout <<"Doe" << endl;}
    // BULKHOURS.REMOVE:END

    void setMyNum(int yourNum) {myNum = yourNum;}
    int getMyNum() {return myNum;}
};

void MyClass::getFirstName(){
    cout << "John" << endl;  // BULKHOURS.REPLACE:cout << "..." << endl;
}

MyClass::MyClass(string yourString) {
    myString = yourString; // BULKHOURS.INIT:"";
    }

int main() {
  MyClass myObj;
  myObj.setMyNum(70);
  cout << myObj.getMyNum() <<endl;
}
"""


def test_cell_reset_cpp():
    cinfo = bulkhours.core.LineParser.from_cell_id_user("synthetic", bulkhours.core.tools.REF_USER)
    teacher_data = bulkhours.core.cell_parser.CellParser.crunch_data(
        cinfo=cinfo, user=bulkhours.core.tools.REF_USER, data=cell_content_cpp
    )
    print(teacher_data.minfo)
    code = teacher_data.get_reset()
    print(code)

    for s in [
        "BK ROCKS",
        "student_evaluation_function",
        "student_hint_function",
        "student_explanation_function",
    ]:
        if s in code:
            raise Exception(f"Should not be here ({s})")


def test_cell_solution_cpp():
    cinfo = bulkhours.core.LineParser.from_cell_id_user("synthetic", bulkhours.core.tools.REF_USER)
    teacher_data = bulkhours.core.cell_parser.CellParser.crunch_data(
        cinfo=cinfo, user=bulkhours.core.tools.REF_USER, data=cell_content_cpp
    )
    code = teacher_data.get_solution()
    print(code)

    if "BULKHOURS." in code:
        raise Exception("Should not be here")

    if "...COMMENT..." in code:
        raise Exception("Should not be here")

    if "student_evaluation_function" in code:
        raise Exception("Should not be here")
