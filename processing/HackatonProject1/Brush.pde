
class Brush {
  ArrayList<PVector> history = new ArrayList<PVector>();   

  PVector location;
  PVector velocity;
  PVector acceleration;
  float r;
  float maxforce;   
  float maxspeed;    
  //true if the brush is drawing
  boolean drawing;
  int currentStroke;
  color currentStrokeColor;

  Brush(float x, float y) {
    acceleration = new PVector(0,0);
    velocity = new PVector(0,-2);
    location = new PVector(x,y);
    r = 6;
    maxspeed = 4;
    maxforce = 10;
    drawing = false;
    currentStroke = 1;
    currentStrokeColor = 0;
  }

  //use to update the location
  void update() {
    velocity.add(acceleration);
    velocity.limit(maxspeed);
    location.add(velocity);
    acceleration.mult(0);
    
    if ( drawing ) {
      history.add(location.get());
      
      if (history.size() > 80) {
        history.remove(0);
      }
    }
  }

  void applyForce(PVector force) {
    acceleration.add(force);
  }

  // STEER = DESIRED MINUS VELOCITY
  //seeking method 
  void seek(PVector target) {
    PVector desired = PVector.sub(target,location);  
    
    desired.normalize();
    desired.mult(maxspeed);
    // Steering = Desired minus velocity
    PVector steer = PVector.sub(desired,velocity);
    steer.limit(maxforce); 
    applyForce(steer);
  }
    
  void display() {
    //re-paint the previous 100 points
    beginShape();
    stroke(currentStrokeColor);
    strokeWeight(currentStroke);
    noFill();
    for(PVector v: history) {
      ellipse(v.x,v.y, 3, 3);
    }
    endShape();
  }
}
