#include <iostream>
#include <cstdlib>
#include <time.h>
using namespace std;
 
// C++ program to find Moore-Penrose inverse  matrix
 
 
#define N 7
 
void Trans_2D_1D(float matrix_2D[N][N], float *matrix) {
 
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            matrix[i * N + j] = matrix_2D[i][j];
        }
        cout<<endl;
    }
 
    return;
 
}
 
 
 
 
void Transpose(float *matrix, float *t_matrix) {
 
 
    for (int i = 0; i<N; i++) {
        for (int j = 0; j<N; j++) {
             t_matrix[j * N + i]=matrix[i * N + j];
 
        }
        cout<<endl;
    }
 
    return;
 
}
 
 
 
void MatrixMult(float *matrix_1, float *matrix_2, float *matrix_product) {
    int k;
    for (int i = 0; i<N; i++) {
        for (int j = 0; j<N; j++) {             // not j<M
            matrix_product[i * N + j] = 0;
            for (k = 0; k<N; k++) {
                matrix_product[i * N + j] += matrix_1[i * N + k] * matrix_2[k * N + j];
            }
        }
    }
     return;
 
}
 
 
 
// Function to get cofactor 
void getCofactor(float *A, float *temp, int p, int q, int n)
{
    int i = 0, j = 0;
 
    // Looping for each element of the matrix
    for (int row = 0; row < n; row++)
    {
        for (int col = 0; col < n; col++)
        {
            // Copying into temporary matrix only those element
            // which are not in given row and column
            if (row != p && col != q)
            {
                temp[i * N + j++] = A[row * N + col];
 
                // Row is filled, so increase row index and
                // reset col index
                if (j == n - 1)
                {
                    j = 0;
                    i++;
                }
            }
        }
    }
}
 
// Recursive function for finding determinant of matrix.
int determinant(float *A, int n)
{
    int D = 0; // Initialize result
 
    // Base case : if matrix contains single element
    if (n == 1)
        return A[0];
 
    float temp[N*N]; // To store cofactors
 
    int sign = 1; // To store sign multiplier
 
    // Iterate for each element of first row
    for (int f = 0; f < n; f++)
    {
        // Getting Cofactor of A[0][f]
        getCofactor(A, temp, 0, f, n);
        D += sign * A[0 * N + f] * determinant(temp, n - 1);
 
        // terms are to be added with alternate sign
        sign = -sign;
    }
 
    return D;
}
 
// Function to get adjoint
void adjoint(float *A,float *adj)
{
    if (N == 1)
    {
        adj[0] = 1;
        return;
    }
 
    // temp is used to store cofactors 
    int sign = 1;
    float temp[N*N];
 
    for (int i=0; i<N; i++)
    {
        for (int j=0; j<N; j++)
        {
            // Get cofactor
            getCofactor(A, temp, i, j, N);
 
            // sign of adj positive if sum of row
            // and column indexes is even.
            sign = ((i+j)%2==0)? 1: -1;
 
            // Interchanging rows and columns to get the
            // transpose of the cofactor matrix
            adj[j * N + i] = (sign)*(determinant(temp, N-1));
        }
    }
}
 
// Function to calculate and store inverse, returns false if
// matrix is singular
bool inverse(float *A, float *inverse)
{
    // Find determinant of A[][]
    int det = determinant(A, N); 
    if (det == 0)
    {
        cout << "Singular matrix, can't find its inverse";
        return false;
    }
 
    // Find adjoint
    float adj[N*N];
    adjoint(A, adj);
 
    // Find Inverse using formula "inverse(A) = adj(A)/det(A)"
    for (int i=0; i<N; i++)
        for (int j=0; j<N; j++)
            inverse[i * N + j]= adj[i * N + j]/float(det);
 
    return true;
}
 
// Generic function to display the matrix. We use it to display
// both adjoin and inverse. adjoin is integer matrix and inverse
// is a float.
template<class T>
void display(T *A)
{
    for (int i=0; i<N; i++)
    {
        for (int j=0; j<N; j++)
            cout << A[i * N + j] << " ";
        cout << endl;
    }
}
 
// Driver program
int main()
{
    float A[N][N] = { {5, -2, 2, 7,9,8,0},
                          {1, 0, 0, 3,1,0,9},
                  {-3, 1, 5, 0,2,1,7},
                  {3, -1, -9, 4,6,5,2},
              {1, 0, 4, 4,1,0,9},
                  {8, 0, 3, 8,6,5,2},
                  {5, 6, 4, 1,3,2,0}
            };
 
    float *matrix = new float[N*N];
    float *t_matrix= new float[N*N];
    float *matrix_mult= new float[N*N];
    float *pseudoinverse= new float[N*N];
    float *adj= new float[N*N]; // To store adjoint 
    float *inv= new float[N*N]; // To store inverse 
 
 
    Transpose(matrix,t_matrix);
    cout << "\nThe Transpose is :\n";
    display(t_matrix);
 
    cout << "The product of the matrix is: " << endl;
    MatrixMult(t_matrix,matrix,matrix_product);
    display(matrix_product);
 
    cout << "\nThe Inverse is :\n";
    if (inverse(matrix_mult, inv))
        display(inv);
 
    MatrixMult(inv,t_matrix,pseudoinverse);
    cout << "\nThe Monroe-penrose inverse is :\n";
    display(pseudoinverse);
 
    return 0;
}