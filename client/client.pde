import processing.net.*;
Client c;
String data;
int data1[];
color col;
 
void setup() {
  size(200, 200);
  c = new Client(this, "127.0.0.1", 50007);
  c.write("GET / HTTP/1.0\r\n");
  c.write("\r\n");
}
 
void draw() {
  if (c.available() > 0) {
    data = c.readString();
    data1 = int(split(data, ' '));
    
  }
  col=color(data1[0],data1[1],data1[2]);
  background(col);
  print(data1[1]);
}
