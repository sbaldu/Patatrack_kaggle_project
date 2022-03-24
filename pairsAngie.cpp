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

std::vector<std::vector<int> > combine(std::vector<int> indexes) {
    std::vector<std::vector<int> > pairs;

    for(int i = 0; i < indexes.size(); ++i) {
        for(int j = i+1; j < indexes.size(); ++j) {
            std::vector<int> pair_to_add;
            pair_to_add.push_back(indexes[i]);
            pair_to_add.push_back(indexes[j]);
            pairs.push_back(pair_to_add);

        }
    }
    return pairs;
}

int return_index(std::vector<int> pair, std::vector<std::vector<int> > pairs) {
    std::vector<int> inv_pair;
    inv_pair.push_back(pair[1]);
    inv_pair.push_back(pair[0]);
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
void printVec(std::vector<double> vec) {
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
    
    // Remove all duplicates from particle_hits
    std::vector<double> particle_types = particles_hits;
    std::sort( particle_types.begin(), particle_types.end() );
    particle_types.erase( std::unique( particle_types.begin(), particle_types.end() ), particle_types.end() );

    // Loop over indexes and make doublets
    std::vector<int> indexes = globalIndexes;
    std::sort(indexes.begin(), indexes.end());
    indexes.erase( std::unique( indexes.begin(), indexes.end() ), indexes.end() );

    std::vector<std::vector<int> > pair_combinations = combine(indexes);
    std::vector<std::vector<int> > pairIndexes;

    for(int i = 0; i < particle_types.size(); ++i) {
        //std::cout << i << '\n';
        if(particle_types[i] != 0) {
            std::vector<int> par_hit_indices;
            par_hit_indices = sort_hits(particle_types[i],particles_hits);
            //printVec(par_hit_indices);

            std::vector<std::vector<int> > pairs_;
            for(int j = 0; j < par_hit_indices.size() - 1; ++j) {
                if(globalIndexes[par_hit_indices[j]] != globalIndexes[par_hit_indices[j+1]]) {
                    std::vector<int> pair_I_will_add;
                    pair_I_will_add.push_back(globalIndexes[par_hit_indices[j]]);
                    pair_I_will_add.push_back(globalIndexes[par_hit_indices[j+1]]);
                pairs_.push_back(pair_I_will_add);
                }
            }
            //for (int j = 0; j < pairs_.size(); ++j) {
            //    std::cout << '[' << pairs_[j][0] << ',' << pairs_[j][1] << ']' << '\n';
            //}
    
            // Give to each pair its index
            std::vector<int> pair_indexes_;
            for(int j = 0; j < pairs_.size(); ++j) {
                pair_indexes_.push_back(return_index(pairs_[j],pair_combinations));
            }
            pairIndexes.push_back(pair_indexes_);
        }  
    }

    std::ofstream outFile;
    outFile.open("hist.csv");
    outFile << "pairIndex" << '\n';

    for(int i = 0; i < pairIndexes.size(); ++i) {
        for(int j = 0; j < pairIndexes[i].size(); ++j) {
            outFile << pairIndexes[i][j] << '\n';
        }
    }
    outFile.close();
} 