JSONArray values;
int R[];
int G[];
int B[];
color c;
void setup() {

  values = loadJSONArray("string.json");
  int R[]=new int[values.size()];
  int G[]=new int[values.size()];
  int B[]=new int[values.size()];
  for (int i = 0; i < values.size(); i++) {
    
     JSONObject rgb = values.getJSONObject(i); 
     R[i] = rgb.getInt("R");
     G[i] = rgb.getInt("G");
     B[i] = rgb.getInt("B");
   
    println(R[i],G[i],B[i]);
  }
  c=color(R[0],B[0],G[0]);
}

void draw(){ 
  
  background(c);
}
