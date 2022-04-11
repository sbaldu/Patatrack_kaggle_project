#include "Framework/EventSetup.h"
#include "Framework/Event.h"
#include "Framework/PluginFactory.h"
#include "Framework/EDProducer.h"
#include "Framework/RunningAverage.h"

#include "CAHitNtupletGeneratorOnGPU.h"
#include "CUDADataFormats/PixelTrackHeterogeneous.h"
#include "CUDADataFormats/TrackingRecHit2DHeterogeneous.h"
#include <fstream>

std::string path = "/home/simonb/documents/thesis/not_sorted/";

class myClass : public edm::EDProducer {
public:
  explicit myClass(edm::ProductRegistry& reg);
  ~myClass() override = default;
  void acquire_single_event(int file_number);
  std::vector<double> get_x();
  std::vector<double> get_y();
  std::vector<double> get_z();
  std::vector<double> get_r();
private:
  void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) override;
  std::vector<double> hits_x_coordinates;
  std::vector<double> hits_y_coordinates;
  std::vector<double> hits_z_coordinates;
  std::vector<double> hits_r_coordinates;
  //edm::EDGetTokenT<TrackingRecHit2DCPU> tokenHitCPU_;
  //edm::EDPutTokenT<PixelTrackHeterogeneous> tokenTrackCPU_;

  CAHitNtupletGeneratorOnGPU gpuAlgo_;
};

myClass::myClass(edm::ProductRegistry& reg)
    : gpuAlgo_(reg) {}

void myClass::produce(edm::Event& iEvent, const edm::EventSetup& es) {
  std::cout << "I'm here!" << '\n';
}

void myClass::acquire_single_event(int file_number) {
  int event_identifier = file_number + 4590;
  
  if(event_identifier >= 5000 && event_identifier < 5500) {
    std::cout << "This file is missing" << '\n';
  } else {
    // Check that the number of hits in c++ is the same that you have in python
    // Make a function that prints all the hits for a single layer
    // Sort also by phi (atg(y/x))
    std::string x_file_name = path + "x_ns" + std::to_string(file_number) + ".dat";
    std::string y_file_name = path + "y_ns" + std::to_string(file_number) + ".dat";
    std::string z_file_name = path + "z_ns" + std::to_string(file_number) + ".dat";
    
    // Read the x_ns*.dat.dat file
    std::ifstream is_1;
    is_1.open(x_file_name);
    int a;

    // Create the vector containing all the x coordinates of the hits
    for(int i = 0; is_1 >> a; ++i) { hits_x_coordinates.push_back(a); }
    is_1.close();

    // Read the y_ns*.dat.dat file
    std::ifstream is_2;
    is_2.open(y_file_name);
    int b;

    // Create the vector containing all the y coordinates of the hits
    for(int i = 0; is_2 >> b; ++i) { hits_y_coordinates.push_back(b); }
    is_2.close();

    // Read the z_ns*.dat.dat file
    std::ifstream is_3;
    is_3.open(z_file_name);
    int c;

    // Create the vector containing all the x coordinates of the hits
    for(int i = 0; is_3 >> c; ++i) { hits_z_coordinates.push_back(c); }
    is_3.close();

    for(int i = 0 ; i < static_cast<int>(hits_y_coordinates.size()); ++i) {
      hits_r_coordinates.push_back(sqrt(pow(hits_y_coordinates[i],2) + pow(hits_z_coordinates[i],2)));
    }
  }
}

std::vector<double> myClass::get_x() { return hits_x_coordinates; }
std::vector<double> myClass::get_y() { return hits_y_coordinates; }
std::vector<double> myClass::get_z() { return hits_z_coordinates; }
std::vector<double> myClass::get_r() { return hits_r_coordinates; }

DEFINE_FWK_MODULE(myClass);