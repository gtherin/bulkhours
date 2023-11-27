rm -rf git_equation && mkdir -p git_equation
cd git_equation/
git init

cp ../git_equation.sh .
echo "a=x*(4)" > a.txt
echo "b=x*(2+3)" > b.txt
echo "a+1=b+1" > equation.txt
git add . && git commit -m "Add equation"

cd ..
zip -r git_equation.zip git_equation
rm -rf git_equation