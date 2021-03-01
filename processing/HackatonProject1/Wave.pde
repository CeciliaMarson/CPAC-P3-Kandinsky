// Wave as concatenation of arcs

class Wave extends Figure {
  //Data
  boolean up = true; // to determine if the arc is concave or convex
  int idx = 0;
  
  //Constructor 
  Wave(Pair p1, Pair p2, Pair p3, color c){
    this.p1 = p1; // position of the center of the first arc
    this.p2 = p2; // w and h of every arc
    this.p3 = p3; // p3.x --> number of iterations | p3.y --> type of wave 
    //NB: The type of wave can be interpreted as:
      // p3.y != 0 --> all arcs are concave
      // p3.y = 0 --> convex and concave arcs are alternating (like a sinusoid)
    this.c = c; // color stroke
    
  }
      
  //Functionalities
  
  void display(){
    stroke(0, random(255)); // we can also stroke this.c
    strokeWeight(random(5));
    noFill();
    
    while(idx < this.p3.x){
      
      if(up || this.p3.y != 0){
        arc((idx*this.p2.x)+this.p1.x,this.p1.y,this.p2.x,this.p2.y,-PI,0); 
      }
      else{
        arc((idx*this.p2.x)+this.p1.x,this.p1.y,this.p2.x,this.p2.y,0,PI);
      }
      
      up = !up; 
      idx++;
    }
  }
}
