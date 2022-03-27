#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <set>
#include <string>
#include <iomanip>
#include <map>

/*
struct Layer{
    int volume_;
    int layer_;
};
*/


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

/*
Layer getKey(std::map<Layer,int> index_map_, int value_) {
    auto it = index_map_.begin();
    auto last = index_map_.end();

    for(; it != last; ++it) {
        if(it->second == value_) {
            return (it->first);
        }
    }
}
*/
std::vector<int> getkey(std::map<std::vector<int>, int> index_map_, int value_) {
    auto it = index_map_.begin();
    auto last = index_map_.end();

    for(; it != last; ++it) {
        if(it->second == value_) {
            return (it->first);
        }
    }

    return {};
}

int main() {
    // I define the map that links the pairs and their indexes
    std::map<std::set<int>, int> pairs_map;
    
    // Fill a vector with all the possible pairs
    std::vector<int> indexes_;
    int max_index = 47;
    for(int i = 0; i <= max_index; ++i ) {
        indexes_.push_back(i);
    }
    std::vector<std::vector<int>> possible_pairs = combine(indexes_);

    // Fill the map
    for(int i = 0; i < possible_pairs.size(); ++i) {
        std::set<int> set_;
        set_.insert(possible_pairs[i][0]);
        set_.insert(possible_pairs[i][1]);
        pairs_map[set_] = i;
    }
    
    // Define a map for the layer global index
    //std::map<Layer,int> index_map;
    std::map<std::vector<int>, int> index_map;

    index_map[{7,2}] = 0;
    index_map[{7,4}] = 1;
    index_map[{7,6}] = 2;
    index_map[{7,8}] = 3;
    index_map[{7,10}] = 4;
    index_map[{7,12}] = 5;
    index_map[{7,14}] = 6;
    index_map[{8,2}] = 7;
    index_map[{8,4}] = 8;
    index_map[{8,6}] = 9;
    index_map[{8,8}] = 10;
    index_map[{9,2}] = 11;
    index_map[{9,4}] = 12;
    index_map[{9,6}] = 13;
    index_map[{9,8}] = 14;
    index_map[{9,10}] = 15;
    index_map[{9,12}] = 16;
    index_map[{9,14}] = 17;
    index_map[{12,2}] = 18;
    index_map[{12,4}] = 19;
    index_map[{12,6}] = 20;
    index_map[{12,8}] = 21;
    index_map[{12,10}] = 22;
    index_map[{12,12}] = 23;
    index_map[{13,2}] = 24;
    index_map[{13,4}] = 25;
    index_map[{13,6}] = 26;
    index_map[{13,8}] = 27;
    index_map[{14,2}] = 28;
    index_map[{14,4}] = 29;
    index_map[{14,6}] = 30;
    index_map[{14,8}] = 31;
    index_map[{14,10}] = 32;
    index_map[{14,12}] = 33;
    index_map[{16,2}] = 34;
    index_map[{16,4}] = 35;
    index_map[{16,6}] = 36;
    index_map[{16,8}] = 37;
    index_map[{16,10}] = 38;
    index_map[{16,12}] = 39;
    index_map[{17,2}] = 40;
    index_map[{17,4}] = 41;
    index_map[{18,2}] = 42;
    index_map[{18,4}] = 43;
    index_map[{18,6}] = 44;
    index_map[{18,8}] = 45;
    index_map[{18,10}] = 46;
    index_map[{18,12}] = 47;

    int n_files = 1769;
    for(int n = 0; n <= n_files; ++n) {
        std::string par_hit_file = "/home/simonb/documents/thesis/not_sorted/par_hits_ns" + std::to_string(n) + ".dat";
        std::string index_file_name = "/home/simonb/documents/thesis/not_sorted/globalIndexes_ns" + std::to_string(n) + ".dat";

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
        std::string hist_file_name = "/home/simonb/documents/thesis/not_sorted/hist_ns" + std::to_string(n) + ".csv";
        outFile.open(hist_file_name);
        outFile << "pairIndex" << ',' << "pair" << ',' << "volume1" << ',' << "volume2" << ',' << "layer1" << "layer2" << ',' << '\n';

        //std::vector<int> pair_indexes_;
        for(int j = 0; j < pairs_.size(); ++j) {
            //pair_indexes_.push_back(return_index(pairs_[j],pair_combinations));
            std::set<int> set_ = {pairs_[j][0],pairs_[j][1]};
            // outFile << return_index(pairs_[j],pair_combinations) << ',' << << ',' << << ',' << << '\n';
            outFile << pairs_map[set_] << ',' << '(' + std::to_string(pairs_[j][0]) + '-' + std::to_string(pairs_[j][1]) +  ')' 
            << ',' << getkey(index_map,pairs_[j][0])[0] << ',' << getkey(index_map,pairs_[j][1])[0] << ',' 
            << getkey(index_map,pairs_[j][0])[1] << ',' << getkey(index_map,pairs_[j][1])[1] <<'\n';
        }
        outFile.close();
   }
}