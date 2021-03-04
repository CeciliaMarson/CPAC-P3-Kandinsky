class Figure{
  //Data
  
  //position 
  Pair p1;
  Pair p2;
  Pair p3;
  color c;
  float opacity;
  int strokeWeight;
  
  //shape object
  PShape shape;
  //stroke color
  int strokeColor;
  //fill of line
  boolean fill;
  //drawable or not
  boolean isDrawable;
  
  //empty constructor 
  Figure(){
  }
  
  //constructor
  Figure(Pair p1, Pair p2, Pair p3, color c, float opacity, int stroke){
      this.p1 = p1;
      this.p2 = p2;
      this.p3 = p3;
      this.c = c;
      this.opacity = opacity;
      this.strokeWeight = stroke;
      this.isDrawable = false;
  }
  
  Figure(Pair p1, color c, float opacity, int stroke, color strokeColor){
      this.p1 = p1;
      this.c = c;
      this.opacity = opacity;
      this.strokeWeight = stroke;
      this.strokeColor = strokeColor;
      this.isDrawable = true;
  }
  
  PVector getVertex(int vertexNum) {
      return this.shape.getVertex(vertexNum);
  } 
  
  int vertexNumber(){
      return this.shape.getVertexCount();
  }
  
  //to be overidden
  void display() {
  
  }
      
}
