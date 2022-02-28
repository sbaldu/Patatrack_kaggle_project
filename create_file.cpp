#include "TTree.h"
#include "TCanvas.h"
#include "TH1F.h"

int main() {
    TTree* t = new TTree("t", "Albero");
    t->ReadFile("test.csv","x/D:y:z");

    t->Draw("x:y:z");
}