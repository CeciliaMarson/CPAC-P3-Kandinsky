class Circle extends Figure {
  //Constructor 
  Circle(Pair p1, float radius, color c, float opacity, int stroke){
    super(p1, c, opacity, stroke, 0);
    this.fill = true;
    
    this.shape = createShape();
    this.shape.beginShape();
    this.shape.fill(c, this.opacity);
  
    for (int i = 0; i < 100; ++i){
        float angle = ((float) i / 100) * TWO_PI;
        this.shape.vertex(cos(angle)*radius +this.p1.x, sin(angle)*radius+this.p1.y);
    }
    
    this.shape.endShape();
  }
      
  //Functionalities
  void display(){
    shape(this.shape);
  }
  
}
