class Grid extends Figure {
  //Data
  int M = 3; // MxM cells in the grid
  
  float x1 = 10, y1 = 10, x2 = 40, y2 = 200; //first vertical line
  float x3 = x1, y3 = y1, x4 = 250, y4 = 20; //first horizontal line
  
  float [][] coord_h_s = new float[M+1][2]; // coordinates of horizontal and vertical, start and end points
  float [][] coord_h_e = new float[M+1][2];
  float [][] coord_v_s = new float[M+1][2];
  float [][] coord_v_e = new float[M+1][2];
  
  float offset_vert = (y2-y1)/M;
  float offset_hor = (x4-x3)/M;
  
  float coeff = 0.8;
  int rand = int(random(100));
  
  color[] c_arr = new color[4];
  
  //Constructor 
  Grid(Pair p1, Pair p2, Pair p3, color c){
    this.p1 = p1; // position of the top left corner 
    this.p2 = p2; // R1, G1 // 2 colors for the square
    this.p3 = p3; // x--> B1 | y --> useless
    this.c = c; // color 
    
    c_arr[0] = color(255, 255, 255); 
    c_arr[1] = color(this.p2.x%255, this.p2.y%255, this.p3.x%255);
    c_arr[2] = color(random(255), random(255), random(255)); // IT CAN BE CHANGED 
    c_arr[3] = this.c;
    
    coord_v_s[0][0] = x1 + this.p1.x; coord_v_s[0][1] = y1 + this.p1.y;
    coord_v_e[0][0] = x2 + this.p1.x; coord_v_e[0][1] = y2 + this.p1.y;  
    coord_h_s[0][0] = x3 + this.p1.x; coord_h_s[0][1] = y3 + this.p1.y;
    coord_h_e[0][0] = x4 + this.p1.x; coord_h_e[0][1] = y4 + this.p1.y;
    
    for (int j=1; j<M+1; j++){
      // x coordinates
      coord_v_s[j][0] = coord_v_s[j-1][0] + offset_hor;
      coord_v_e[j][0] = coord_v_e[j-1][0] + offset_hor*coeff;
      coord_h_s[j][0] = coord_h_s[j-1][0];
      coord_h_e[j][0] = coord_h_e[j-1][0];
      
      // y coordinates
      coord_v_s[j][1] = coord_v_s[j-1][1];
      coord_v_e[j][1] = coord_v_e[j-1][1];
      coord_h_s[j][1] = coord_h_s[j-1][1] + offset_vert;
      coord_h_e[j][1] = coord_h_e[j-1][1] + offset_vert*coeff;  
    
    }

    
  }
     
  //Functionalities
  
  void display(){
    
    for(int i=0; i<M; i++){ // i-->horizontal index
      for(int j=0; j<M; j++){ // v-->vertical index
        
          Pair hit0 = lineLine(coord_v_s[j][0], coord_v_s[j][1], coord_v_e[j][0], coord_v_e[j][1], coord_h_s[i][0], coord_h_s[i][1], coord_h_e[i][0], coord_h_e[i][1]);
          Pair hit1 = lineLine(coord_h_s[i][0], coord_h_s[i][1], coord_h_e[i][0], coord_h_e[i][1], coord_v_s[j+1][0], coord_v_s[j+1][1], coord_v_e[j+1][0], coord_v_e[j+1][1]);
          Pair hit2 = lineLine(coord_v_s[j+1][0], coord_v_s[j+1][1], coord_v_e[j+1][0], coord_v_e[j+1][1], coord_h_s[i+1][0], coord_h_s[i+1][1], coord_h_e[i+1][0], coord_h_e[i+1][1]);
          Pair hit3 = lineLine(coord_h_s[i+1][0], coord_h_s[i+1][1], coord_h_e[i+1][0], coord_h_e[i+1][1], coord_v_s[j][0], coord_v_s[j][1], coord_v_e[j][0], coord_v_e[j][1]);
      
          stroke(0);
          strokeWeight(2);
          fill(c_arr[(i+1)*(j+1)%4]);
          quad(hit0.x, hit0.y, hit1.x, hit1.y, hit2.x, hit2.y, hit3.x, hit3.y);
      }
    }
    
  }
  
  Pair lineLine(float x1, float y1, float x2, float y2, float x3, float y3, float x4, float y4) {
    // calculate the distance to intersection point
    float uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1));
    float uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1));
    
    Pair intersection = new Pair(0, 0);
  
    // if uA and uB are between 0-1, lines are colliding
    if (uA >= 0 && uA <= 1 && uB >= 0 && uB <= 1) {
  
      // optionally, draw a circle where the lines meet
      float intersectionX = x1 + (uA * (x2-x1));
      float intersectionY = y1 + (uA * (y2-y1));
      intersection = new Pair(intersectionX, intersectionY);
      //fill(255,0,0);
      //noStroke();
      //ellipse(intersectionX,intersectionY, 5,5);
  
      return intersection;
    }
    return intersection; //handle error, no intersection
  }
  
  
}
