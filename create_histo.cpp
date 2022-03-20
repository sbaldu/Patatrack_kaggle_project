void patata() {
    TTree *t = new TTree("Pippo","Pluto"); 
    t->ReadFile("hist.csv","pairIndex/D");
    t->Draw("pairIndex");
}