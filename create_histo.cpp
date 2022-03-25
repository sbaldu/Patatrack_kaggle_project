void histo() {
    TTree *t = new TTree("Pippo","Pluto"); 
    t->ReadFile("/home/simonb/Documents/thesis/doublet_files/hist0.csv","pairIndex/D");
    t->Draw("pairIndex");
}