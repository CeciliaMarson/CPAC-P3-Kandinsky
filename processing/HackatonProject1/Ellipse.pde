class Ellipse extends Figure {
  
    //Constructor 
    Ellipse(Pair p1, float a, float b, color c, float opacity, int stroke){
    super(p1, c, opacity, stroke, 0);
    this.fill = true;
    
    this.shape = createShape();
    this.shape.beginShape();
    this.shape.fill(this.c, this.opacity);
    
    for (int i = 0; i < 100; ++i) { 
      float angle = ((float) i / 100) * TWO_PI;
      this.shape.vertex(cos(angle)*a +this.p1.x, sin(angle)*b+this.p1.y);
    }
      
    this.shape.endShape();
  }
      
  //Functionalities
  void display(){
    shape(this.shape);
  }
  
}
