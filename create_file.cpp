#include <iostream>
#include <fstream>
#include <vector>

int main() {
    std::ifstream is;
    is.open("indexes.dat");
    std::vector<int> indexes;
    int a;

    for(int i = 0; is >> a; ++i) {
        indexes.push_back(a);
    }

    is.close();
    int size_ = indexes.size();
    std::vector<std::vector<int>> pairs;

    for(int i = 0; i < size_-1; ++i) {
        if(indexes[i] != indexes[i+1]) {
            pairs.push_back({indexes[i],indexes[i+1]});
        }
    }

    int n_pairs = pairs.size();
    for(int i; i < n_pairs; ++i) {
        std::cout << '[' << pairs[i][0] << ',' << pairs[i][1] << ']' << '\n';
    }
}