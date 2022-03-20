#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <set>

std::vector<int> sort_hits(double particle_id, std::vector<double> par_hits_) {
    std::vector<int> result;

    for(int i = 0; i < par_hits_.size(); ++i) {
        if(par_hits_[i] == particle_id) {
            result.push_back(i);
        }
    }
            
    return result;
}

bool is_in_vec(int input_, std::vector<int> vec_) {
    for (int i = 0; i < vec_.size(); ++i) {
        if(vec_[i] == input_) {
            return true;
        }
    }

    return false;
}

std::vector<std::vector<int>> combine(std::vector<int> indexes) {
    std::vector<std::vector<int>> pairs;

    for(int i = 0; i < indexes.size(); ++i) {
        for(int j = i+1; j < indexes.size(); ++j) {
            pairs.push_back({indexes[i],indexes[j]});
        }
    }
    return pairs;
}

int return_index(std::vector<int> pair, std::vector<std::vector<int>> pairs) {
    std::vector<int> inv_pair{pair[1],pair[0]};
    for(int i = 0; i < pairs.size(); ++i) {
        if((pair == pairs[i]) || (inv_pair == pairs[i])) {
            return i;
        }
    }
    return 12345;
}

void printVec(std::vector<int> vec) {
    for(int i = 0; i < vec.size(); ++i) {
        std::cout << vec[i] << '\n';
    }
}

int main() {
    // Read the par_hits.dat file
    std::ifstream is;
    is.open("par_hits.dat");
    std::vector<double> particles_hits;
    double a;

    // Create the vector containing all the particle ids (particle_id column in the df)
    for(int i = 0; is >> a; ++i) {
       particles_hits.push_back(a);
    }
    is.close();
    
    std::cout << particles_hits[0] << '\n';
    std::cout << sort_hits(612491885784596480,particles_hits)[0] << '\n';

    // Read the globalIndex.dat file
    std::ifstream is2;
    is2.open("globalIndexes.dat");
    std::vector<int> globalIndexes;
    int b;

    // Create the vector containing all the global indexes (globalIndex column in the df)
    for(int i = 0; is2 >> b; ++i) {
        globalIndexes.push_back(b);
    }
    is2.close();
    
    //printVec(globalIndexes);
    // Remove all duplicates from particle_hits
    std::vector<double> particle_types = particles_hits;
    std::sort( particle_types.begin(), particle_types.end() );
    particle_types.erase( std::unique( particle_types.begin(), particle_types.end() ), particle_types.end() );
    //std::cout << particle_types.size() << '\n';

    // Loop over indexes and make doublets
    std::vector<int> indexes = globalIndexes;
    std::sort( indexes.begin(), indexes.end() );
    indexes.erase( std::unique( indexes.begin(), indexes.end() ), indexes.end() );
    std::cout << indexes.size() << '\n';
    //printVec(indexes);

    std::vector<std::vector<int>> pair_combinations = combine(indexes);
    //for(int i = 0; i < pair_combinations.size(); ++i) {
    //    std::cout << '[' << pair_combinations[i][0] << ',' << pair_combinations[i][1] << ']' << '\n';
    //}
    std::vector<std::vector<int>> pairIndexes;

    for(int i = 0; i < particle_types.size()-8976; ++i) {
        std::vector<int> hits_global_indexes;
        hits_global_indexes = sort_hits(particle_types[i],particles_hits);
        printVec(hits_global_indexes);

        std::vector<std::vector<int>> pairs_;
        for(int j = 0; j < hits_global_indexes.size() - 1; ++j) {
            if(hits_global_indexes[j] != hits_global_indexes[j+1]) {
                pairs_.push_back({hits_global_indexes[j],hits_global_indexes[j+1]});
            }
        }
    
        // Give to each pair it's index
        std::vector<int> pair_indexes_;
        for(int j = 0; j < pairs_.size(); ++j) {
            pair_indexes_.push_back(return_index(pairs_[j],pair_combinations));
        }
        pairIndexes.push_back(pair_indexes_);
    }

    for(int i = 0; i < pairIndexes.size(); ++i) {
        //printVec(pairIndexes[i]);
    }
}