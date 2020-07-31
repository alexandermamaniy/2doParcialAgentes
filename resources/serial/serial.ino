#include <Servo.h>
#include <NewPing.h>

#define PIN_TRIG 12
#define PIN_ECHO 11
 
#define MAX_DISTANCE 200 // Constante para determinar la distancia máxima, que consideraremos correcta

// Motor A
int ENA = 2;
int IN1 = 4;
int IN2 = 3;

// Motor B
int ENB = 5;
int IN3 = 7;
int IN4 = 6;
int velocidadMotor = 200;
// Declaramos la variable para controlar el servo
Servo servoMotor;
//Declaramos las variables para utilizar el ultrasonico
NewPing sonar(PIN_TRIG, PIN_ECHO, MAX_DISTANCE);

//pines digitales puente h 
int disCm;
int periodo = 500;
unsigned long TiempoAhora = 0;
void setup()
{
  pinMode (ENA, OUTPUT);
  pinMode (ENB, OUTPUT);
  pinMode (IN1, OUTPUT);
  pinMode (IN2, OUTPUT);
  pinMode (IN3, OUTPUT);
  pinMode (IN4, OUTPUT);
  Serial.begin(9600);//iniciailzamos la comunicación
   // Iniciamos el servo para que empiece a trabajar con el pin 12
  servoMotor.attach(8);
  servoMotor.write(20);
  Serial.println("conectado");
}

void loop()
{ 
  //disCm = sonar.ping_cm();
  if(Serial.available() > 0)
  {   
    char dato = Serial.read();
      if (dato == '0'){
        Adelante();
      }
      else if (dato == '1'){
        Derecha();
      }
      else if (dato == '2'){
        Izquierda();
      }
      else if (dato == '3'){
        Parar();
      }
      else if (dato == '4'){
        //giro180();
      }
        else if (dato == '5'){
        Atras();
      }
      else if(dato == 'SA'){
         servoMotor.write(20);
      }
      else if(dato == 'SC'){
         servoMotor.write(60);
      }
  } 
  if(millis() > TiempoAhora + periodo){
        unsigned int distance = sonar.ping_cm();
        if(!isnan(distance)){
           Serial.print(distance);
        }
    }
}
void Atras ()
{
 //Direccion motor A
 digitalWrite (IN1, HIGH);
 digitalWrite (IN2, LOW);
 analogWrite (ENA, velocidadMotor); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, HIGH);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, velocidadMotor); //Velocidad motor B
}
void Adelante ()
{
 //Direccion motor A
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, HIGH);
 analogWrite (ENA, velocidadMotor); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, HIGH);
 analogWrite (ENB, velocidadMotor); //Velocidad motor B
}
void Derecha ()
{
 //Direccion motor A
 digitalWrite (IN1, HIGH);
 digitalWrite (IN2, LOW);
 analogWrite (ENA, velocidadMotor); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, HIGH);
 analogWrite (ENB, velocidadMotor); //Velocidad motor A
}

void Izquierda ()
{
 //Direccion motor A
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, HIGH);
 analogWrite (ENA, velocidadMotor); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, HIGH);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, velocidadMotor); //Velocidad motor A
}
void Parar ()
{
 //Direccion motor A
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, LOW);
 analogWrite (ENA, 0); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, 0); //Velocidad motor A
}