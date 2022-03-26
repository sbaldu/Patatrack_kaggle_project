#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <set>
#include <string>
#include <iomanip>

std::vector<int> sort_hits(double const &particle_id, std::vector<double> &par_hits_) {
    std::vector<int> result;

    for(int i = 0; i < par_hits_.size(); ++i) {
        if(par_hits_[i] == particle_id) {
            result.push_back(i);
            //if(par_hits_[i+1] != particle_id) {
            //    break;
            //}
        }
    }
            
    return result;
}

bool is_in_vec(int &input_, std::vector<int> const &vec_) {
    for (int i = 0; i < vec_.size(); ++i) {
        if(vec_[i] == input_) {
            return true;
        }
    }

    return false;
}

std::vector<std::vector<int>> combine(std::vector<int> const &indexes) {
    std::vector<std::vector<int>> pairs;

    for(int i = 0; i < indexes.size(); ++i) {
        for(int j = i+1; j < indexes.size(); ++j) {
            pairs.push_back({indexes[i],indexes[j]});
        }
    }
    return pairs;
}

int return_index(std::vector<int> const &pair, std::vector<std::vector<int>> const &pairs) {
    std::vector<int> inv_pair{pair[1],pair[0]};
    for(int i = 0; i < pairs.size(); ++i) {
        if((pair == pairs[i]) || (inv_pair == pairs[i])) {
            return i;
        }
    }
    return 12345;
}

void printVec(std::vector<int> const &vec) {
    for(int i = 0; i < vec.size(); ++i) {
        std::cout << vec[i] << '\n';
    }
}
void printVec(std::vector<double> const &vec) {
    for(int i = 0; i < vec.size(); ++i) {
        std::cout << vec[i] << '\n';
    }
}

int main() {
    int n_files = 1769;
    for(int n = 0; n <= n_files; ++n) {
        std::string par_hit_file = "/home/simonb/Documents/thesis/not_sorted/par_hits_ns" + std::to_string(n) + ".dat";
        std::string index_file_name = "/home/simonb/Documents/thesis/not_sorted/globalIndexes_ns" + std::to_string(n) + ".dat";

        // Read the par_hits.dat file
        std::ifstream is;
        is.open(par_hit_file);
        std::vector<double> particles_hits;
        double a;

        // Create the vector containing all the particle ids (particle_id column in the df)
        for(int i = 0; is >> a; ++i) {
            particles_hits.push_back(a);
        }
        is.close();

        // Read the globalIndex.dat file
        std::ifstream is2;
        is2.open(index_file_name);
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

        std::vector<std::vector<int>> pair_combinations = combine(indexes);
        //std::vector<std::vector<int>> pairIndexes;

        std::cout << particle_types.size() << '\n';
        std::vector<std::vector<int>> pairs_;

        for(int i = 0; i < particle_types.size(); ++i) {
            std::vector<int> par_hit_indices = sort_hits(particle_types[i],particles_hits);
            //std::cout << std::fixed;
            //std::cout << std::setprecision(2);
            //std::cout << particle_types[i] << '\n';

            for(int j = 0; j < par_hit_indices.size() - 1; ++j) {
                if(globalIndexes[par_hit_indices[j]] != globalIndexes[par_hit_indices[j+1]]) {
                    pairs_.push_back({globalIndexes[par_hit_indices[j]],globalIndexes[par_hit_indices[j+1]]});
                }
            }
            //std::cout << pairs_.size() << '\n';
            //for(int k = 0; k < pairs_.size(); ++k) {
            //    printVec(pairs_[i]);
            //}      
        }

        // Give to each pair its index and prepare the csv file for the histogram
        std::ofstream outFile;
        std::string hist_file_name = "/home/simonb/Documents/thesis/not_sorted/hist_ns" + std::to_string(n) + ".csv";
        outFile.open(hist_file_name);
        outFile << "pairIndex" << '\n';

        std::vector<int> pair_indexes_;
        for(int j = 0; j < pairs_.size(); ++j) {
            pair_indexes_.push_back(return_index(pairs_[j],pair_combinations));
            outFile << return_index(pairs_[j],pair_combinations) << '\n';
        }
        outFile.close();
   }
}