#include <iostream>
#include <fstream>
#include <vector>


std::vector<int> sort_hits(double particle_id, std::vector<double> par_hits_) {
    std::vector<int> result;

    for(int i = 0; i < par_hits_.size(); ++i) {
        if(par_hits_[i] == particle_id) {
            result.push_back(i);
        }
    }
            
    return result;
}


int main() {
    std::ifstream is;
    is.open("par_hits.dat");
    std::vector<double> particles_hits;
    double a;

    for(int i = 0; is >> a; ++i) {
       particles_hits.push_back(a);
    }
    is.close();
    
    std::cout << particles_hits[0] << '\n';
    std::cout << sort_hits(612491885784596480,particles_hits)[0] << '\n';

    std::ifstream is2;
    is2.open("globalIndex.dat");
    std::vector<int> globalIndexes;
    double b;

    for(int i = 0; is2 >> b; ++i) {
        globalIndexes.push_back(b);
    }



    
    /*
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
    */
}