class Triangle extends Figure {
  /*
  p1 -> position first point
  p2 -> position second point
  p3 -> // position third point (or x --> control | y --> height)
  //control   x = 0 --> equilateral | x=1 --> irregular(scaleno) | x otherwise --> isosceles
  c -> color stroke
  opacity -> alpha
  */
  float x_m, y_m, m, m_p, q_p, a_eq, b_eq, c_eq, h, l;
  float x3, y3;
  
  //Constructor 
  Triangle(Pair p1, Pair p2, Pair p3, color c, float opacity, int stroke){
    super(p1, p2, p3, c, opacity, stroke);
    
    if ( this.p3.x == 0 ) {
      // equilateral triangle
      l = sqrt(pow(this.p2.x-this.p1.x, 2) + pow(this.p2.y-this.p1.y, 2));
      h = l * sqrt(3) / 2;
    }
      else{
        // isosceles triangle
        h = this.p3.y;
      }
    
    x_m = (this.p1.x + this.p2.x)/2; // midpoint coordinates
    y_m = (this.p1.y + this.p2.y)/2;
    
    m = (this.p2.y - this.p1.y)/(this.p2.x - this.p1.x); //slope of the segment
    m_p = -1/m; //slope perpendicular
    
    if (m == 0) {
      //the symmetry axis is parallel to the y axis (verical)
      x3 = x_m;
      y3 = y_m + h;
    }
      else if(m_p == 0){
        //the symmetry axis is parallel to the x axis (horizontal)
        x3 = x_m + h;
        y3 = y_m;
      }
        else{
          q_p = y_m - m_p*x_m; // y intercept of the axis of the segment described by the first two points
          
          a_eq = 1 + pow(m_p, 2); // coefficients of the second order equation
          b_eq = 2*(m_p*q_p - m_p*y_m - x_m);
          c_eq = pow(q_p-y_m, 2) - pow(h, 2) + pow(x_m, 2);
          
          x3 = (-b_eq - sqrt(pow(b_eq, 2) - 4*a_eq*c_eq)) / (2*a_eq); // solution quadratic equation
          y3 = m_p * x3 + q_p; // find the corresponding y3 that lies on the axis
        }
        
    if ( this.p3.x == 1 ) {
      x3 = x3 + random(100);
      y3 = y3 + random(100);
    }
    
  }
      
  //Functionalities
  void display(){
    stroke(0);
    strokeWeight(this.strokeWeight);
    fill(this.c, this.opacity);
    triangle(this.p1.x,this.p1.y,this.p2.x,this.p2.y, x3, y3); //check if this.stuff or variable_in_class
  
  }
}
