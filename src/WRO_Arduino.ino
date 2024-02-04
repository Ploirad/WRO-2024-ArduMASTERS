#include <Servo.h>

//CREAR LOS SERVOS DE DIRECCION (180), CAMARA (180) Y EL MOTRIZ (2 DE 360 JUNTOS)
Servo direccion;
Servo camara;
Servo motriz;

//VARIABLES DE LOS SENSORES DE DISTANCIA
long tA=0;
long dA=0;
long tB=0;
long dB=0;

//SENSOR A
const int TriggerA = 8;
const int EchoA = 9;
int distanciaA;
float tiempoA;

//SENSOR B
const int TriggerB = 10;
const int EchoB = 11;
int distanciaB;
float tiempoB;


char control;
//1: DIRECCION = RECTO
//2: DIRECCION = IZQUIERDA
//3: DIRECCION = DERECHA
//4: RUEDAS = STOP
//5: RUEDAS = AVANCE
//6: RUEDAS = RETROCESO
//7: CAMARA = DELANTE
//8: CAMARA = ATRAS

int grados_direccion = 90;
//90=RECTO
//0=IZQUIERDA
//180=DERECHA

int grados_camara = 0;
//0=NORMAL
//180=CAMBIO DE SENTIDO

int velocidad_ruedas = 90; 
//90=STOP 
// 0=DIRECCION1 
//180=DIRECCION2

void setup() {
  Serial.begin(9600);
  
  //ESTABLECER SERVOS
  direccion.attach(2);//EL SERVO DE DIRECCION VA EN EL PIN 2
  camara.attach(3);//EL SERVO DE LA CAMARA VA EL EL PIN 3
  motriz.attach(5);//EL SERVO MOTRIZ VA EN EL PIN 5
  
  //ESTABLECER SENSORES DE DISTANCIA
  pinMode(TriggerA, OUTPUT);
  pinMode(EchoA, INPUT);
  pinMode(TriggerB, OUTPUT);
  pinMode(EchoB, INPUT);
  digitalWrite(TriggerA, LOW);
  digitalWrite(TriggerB, LOW);}
 
void loop() {
  servos();//TODO LO RELACIONADO CON LOS SERVOS
  sensores_de_distancia();} //TODO LO RELACIONADO CON LOS SENSORES DE DISTANCIA

void servos(){//TODO LO RELACIONADO CON LOS SERVOS
  controlacion();//LEE Y ESCRIBE
  verificacion();}//COMPRUEBA LOS IF'S
    
void controlacion(){ //LEE Y ESCRIBE
  control = Serial.read(); //LEER EL MONITOR SERIAL
  direccion.write(grados_direccion); //MARCAR LOS GRADOS DE LA DIRECCION [0, 90, 180]
  camara.write(grados_camara); //MARCAR LOS GRADOS DE LA CAMARA [0, 180]
  motriz.write(velocidad_ruedas);} //MARCAR LA DIRECCION {PARADO: [90], AVANCE: [180], RETROCESO: [0]}

void verificacion(){ //COMPROBAR LOS IF'S
  verificar_direccion();//IF'S DE LA DIRECCION
  verificar_velocidad();//IF'S DE LA VELOCIDAD DE LAS RUEDAS
  verificar_angulo_camara();}//IF'S DEL ANGULO DEL SERVO DE CAMARA


void verificar_direccion(){//IF'S DE LA DIRECCION
  if(control == '1'){grados_direccion=90;}       //CENTRO
  else if(control == '2'){grados_direccion=0;}   //IZQUIERDA
  else if(control == '3'){grados_direccion=180;}}//DERECHA

void verificar_velocidad(){//IF'S DE LA VELOCIDAD DE LAS RUEDAS
  if(control == '4'){velocidad_ruedas=90;}        //STOP
  else if(control == '5'){velocidad_ruedas=0;}    //AVANCE
  else if(control == '6'){velocidad_ruedas=180;}} //RETROCESO

void verificar_angulo_camara(){//IF'S DEL ANGULO DEL SERVO DE LA CAMARA
  if(control == '7'){grados_camara=0;}        //DE FRENTE
  else if(control == '8'){grados_camara=180;}}//HACIA ATRAS
    
void sensores_de_distancia(){//TODO LO RELACIONADO DE LOS SENSORES DE DISTANCIA
  resetear_variables();//RESETEA TODAS LAS VARIABLES DE LOS SENSORES DE DISTANCIA
  deteccion_distancia();//CALCULA LA DISTANCIA
  imprimir();}//IMPRIME LOS VALORES EN EL MONITOR SERIAL

void resetear_variables(){//RESETEA TODAS LAS VARIABLES DE LOS SENSORES DE DISTANCIA
  tA=0;
  dA=0;
  tB=0;
  dB=0;}

void deteccion_distancia(){//CALCULA LA DISTANCIA
sensorA();//CALCULA EN EL SENSOR A
sensorB();}//CALCULA EN EL SENSOR B
  
void sensorA(){//CALCULA EN EL SENSOR A
  digitalWrite(TriggerA, HIGH);
  delayMicroseconds(10);
  digitalWrite(TriggerA, LOW);
  tA = pulseIn(EchoA, HIGH);
  dA = tA/59;}

void sensorB(){//CALCULA EN EL SENSOR B
  digitalWrite(TriggerB, HIGH);
  delayMicroseconds(10);
  digitalWrite(TriggerB, LOW);
  tB = pulseIn(EchoB, HIGH);
  dB = tB/59;}
  
void imprimir(){//IMPRIME LOS VALORES EN EL MONITOR SERIAL
  Serial.print("D.A: ");
  Serial.print(dA);//DISTANCIA A EN cm
  Serial.print("cm");
  Serial.print("  D.B: ");
  Serial.print(dB);//DISTANCIA B EN cm
  Serial.println("cm");}
