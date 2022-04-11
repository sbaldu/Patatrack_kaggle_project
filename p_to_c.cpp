#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <math.h>
#include <map>
#include <stdio.h>

int main() {

    //CHANGE FOR NECESSARY FILE
    std::string path = "/Users/pfudolig/patatrack/trackml-library-master/trackmlrepo/Patatrack_kaggle_project/" ;
    std::string fname = path + "train_1/event000002819-hits.csv" ;

    std::vector < std::vector <std::string> > content;
    std::vector < std::string> row;
    std::string line, word;

    //user-inputted hit ID for displaying one row of data
    int hit_input, hit_id;
    std::cout << "Enter hit ID: " ;
    std::cin >> hit_input;

    //opens file to use
    std::ifstream file (fname);
    if(file.is_open()) { 
        while(std::getline(file,line)) {
            row.clear();
            std::stringstream str(line);
            while(std::getline(str,word, ',')){
                row.push_back(word);
            }

            
            //displaying just one row of data, works for any hits file
            hit_id = atoi(row[0].c_str());
            if (hit_id == hit_input) {
                std::cout << "Details of Hit ID " << row[0] << ": \n";
                std::cout << "X: " << row[1] << "\n";
                std::cout << "Y: " << row[2] << "\n";
                std::cout << "Z: " << row[3] << "\n";
                std::cout << "Volume ID: " << row[4] << "\n";
                std::cout << "Layer ID: " << row[5] << "\n";
                std::cout << "Module ID: " << row[6] << "\n";
                break;
            }
            

            /*
            //calculating r values of each hit
            int x_int = atoi(row[1].c_str());
            int y_int = atoi(row[2].c_str());
            int z_int = atoi(row[3].c_str());
            int x_sq = pow(x_int,2);
            int y_sq = pow(y_int,2);
            int z_sq = pow(z_int,2);
            int xyz = x_sq + y_sq + z_sq;
            int r = pow(xyz,0.5); //should i make this an array?
            */

            /*
            //creating a global indexing scheme
            int LayerID = atoi(row[5].c_str());
            int MaxLayerID = 7;
            int MaxVolID = 18-7;
            int CompactLayerID = LayerID / 2 - 1; //make this an array?
            int global_index = MaxVolID * (MaxLayerID + 1) + CompactLayerID;
            std::cout << global_index << " "; //looks like it just keeps reprinting, also is 88-93 for some reason
            */
            
            content.push_back(row);
        }
        
    }

//in case of error in accessing file
    else {
        std::cout << "Could not open file";
    }

/*
//displaying whole data table, generalized
    for(int i=0; i<content.size(); i++) {
        for(int j=0; j<content[i].size(); j++) {
            std::cout << content[i][j] << " ";
        }
        std::cout << "\n"; //new line?
    }
*/

/*
//manually-created dictionary of global indices, input Key and output mapped value
    std::map <std::string, int> globalIndex;
    globalIndex["(7,2)"] = 0;
    globalIndex["(7,4)"] = 1;
    globalIndex["(7,6)"] = 2;
    globalIndex["(7,8)"] = 3;
    globalIndex["(7,10)"] = 4;
    globalIndex["(7,12)"] = 5;
    globalIndex["(7,14)"] = 6;
    globalIndex["(8,2)"] = 7;
    globalIndex["(8,4)"] = 8;
    globalIndex["(8,6)"] = 9;
    globalIndex["(8,8)"] = 10;
    globalIndex["(9,2)"] = 11;
    globalIndex["(9,4)"] = 12;
    globalIndex["(9,6)"] = 13;
    globalIndex["(9,8)"] = 14;
    globalIndex["(9,10)"] = 15;
    globalIndex["(9,12)"] = 16;
    globalIndex["(9,14)"] = 17;
    globalIndex["(12,2)"] = 18;
    globalIndex["(12,4)"] = 19;
    globalIndex["(12,6)"] = 20;
    globalIndex["(12,8)"] = 21;
    globalIndex["(12,10)"] = 22;
    globalIndex["(12,12)"] = 23;
    globalIndex["(13,2)"] = 24;
    globalIndex["(13,4)"] = 25;
    globalIndex["(13,6)"] = 26;
    globalIndex["(13,8)"] = 27;
    globalIndex["(14,2)"] = 28;
    globalIndex["(14,4)"] = 29;
    globalIndex["(14,6)"] = 30;
    globalIndex["(14,8)"] = 31;
    globalIndex["(14,10)"] = 32;
    globalIndex["(14,12)"] = 33;
    globalIndex["(16,2)"] = 34;
    globalIndex["(16,4)"] = 35;
    globalIndex["(16,6)"] = 36;
    globalIndex["(16,8)"] = 37;
    globalIndex["(16,10)"] = 38;
    globalIndex["(16,12)"] = 39;
    globalIndex["(17,2)"] = 40;
    globalIndex["(17,4)"] = 41;
    globalIndex["(18,2)"] = 42;
    globalIndex["(18,4)"] = 43;
    globalIndex["(18,6)"] = 44;
    globalIndex["(18,8)"] = 45;
    globalIndex["(18,10)"] = 46;
    globalIndex["(18,12)"] = 47;

    std::string key;
    std::cout << "Enter Key: " ;
    std::cin >> key;
    std::cout << globalIndex[key] << std::endl;
*/

}