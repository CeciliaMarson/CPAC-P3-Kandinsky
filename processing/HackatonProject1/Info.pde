//represent the info required to create a figure
class Info {
  
  //color 
  color col;
  //shape 
  int shape;
  //Opacity
  float opacity;
  //position
  Pair position;
  //stroke weight
  int strokeWeight;
  
  
  Info(color c, int shape, float opacity, Pair pos, int stroke) {
     this.col=c;
     this.shape = shape;
     this.opacity = opacity;
     this.position = pos;
     this.strokeWeight = stroke;
  }
}
