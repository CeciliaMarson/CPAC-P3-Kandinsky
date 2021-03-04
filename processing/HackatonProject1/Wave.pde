class Wave extends Figure {
  
  //Constructor 
  Wave(Pair p1, color c, float opacity, int stroke){
    super(p1, c, opacity, stroke, 0);
    if (int(random(2)) == 0)
      this.fill = true;
    else this.fill = false;
    
    this.shape = createShape();
    this.shape.beginShape();
    if( this.fill ) 
      this.shape.fill(c, this.opacity);
    else this.shape.noFill();
    // Calculate the path as a sine wave
    float x = this.p1.x;
    float stopAngle = random(1.5, 7);
    for (float a = 0; a < stopAngle; a += 0.1) {
      this.shape.vertex(x,sin(a)*100+this.p1.y);
      x+= 5;
    }
    this.shape.endShape();
  }
      
  //Functionalities
  
  void display(){
    shape(this.shape);
  }
}
