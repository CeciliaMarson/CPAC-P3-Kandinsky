class ArcFill extends Figure {
  
  //Constructor 
  ArcFill(Pair p1, color c, float opacity, int stroke){
    super(p1, c, opacity, stroke, 0);
    this.fill = true;
    
    this.shape = createShape();
    this.shape.beginShape();
    this.shape.fill(c, this.opacity);
    // Calculate the path as a sine wave
    float x = this.p1.x;
    float start = random(0, PI);
    float stop = random(PI, 2*PI);
    for (float a = start; a < stop; a += 0.1) {
      this.shape.vertex(x,sin(a)*100+this.p1.y);
      x+= 10;
    }
    this.shape.endShape();
  }
      
  //Functionalities
  void display(){
    shape(this.shape);
  }
}
