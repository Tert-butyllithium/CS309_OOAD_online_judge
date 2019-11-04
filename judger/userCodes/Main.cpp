#include <iostream>
#include <iomanip>
 
using namespace std;
 
int main() {
    int N;
    float M;
    cin >> N;
    M = 0.85 * N;
    cout << setiosflags(ios::fixed);
    cout.precision(2);
    cout << M << endl;
}
