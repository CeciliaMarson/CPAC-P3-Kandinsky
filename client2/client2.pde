import oscP5.*;
import netP5.*;
String value1;
color c;
OscP5 oscP5;
NetAddress myRemoteLocation;
int data[][];
int val[];
int num;
String list[];

void setup() {
  size(400,400);
  frameRate(25);
  oscP5 = new OscP5(this,57121);


  myRemoteLocation = new NetAddress("127.0.0.1", 57121);
}

void draw() {
  background(0);
  c=color(12,3,99);
  
  if(value1 != null){
   
   background(c);
    
   }

}


void oscEvent(OscMessage theOscMessage) {
  value1 = theOscMessage.get(0).stringValue();
  create_data(value1);
}

void create_data(String msg){
  list= split(msg,',');
  for(int i=0; i<list.length; i++){
  val=int(split(list[i],' ')); 
  data[i]=val;
}
}
