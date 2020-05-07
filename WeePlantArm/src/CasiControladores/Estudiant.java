package CasiControladores;

import com.fazecast.jSerialComm.SerialPort;

/***
 * Classe a modificar per l'estudiant de SDM.
 *
 * Nota: S'ha de vincular la carpeta libs al projecte!
 *       JDK 8.0 OBLIGATORI!
 */

public class Estudiant {

    //S'inicialitza automàticament quan es prem el botó -Connect- de la finestra Serial Settings
    public static SerialPort mySerial;

    //Període en ms amb el que es crida la funció readMode().
    public static final int READ_PERIOD = 1000;

    //Període en ms amb el que es crida la funció writeMode() quan l'Animator té activat Writing i es modifica l'angle
    //d'un motor. Serveix per a no cridar wirteMode() infinites vegades al modificar l'angle dels motors.
    public static final long WRITE_PERIOD = 1000;

    //Aquesta funció es crida cada cop que es modifica la posició dels motors en l'Animator i està activada
    //l'opció Writting.
    //Rep els dos angles dels motors com arguments.
    public static void writeMode(int angleMotor1, int angleMotor2){
        System.out.println("Aquí va el codi que escriu en el port sèrie.\nEnviant angles " + angleMotor1 + " " + angleMotor2);
    }

    //Aquesta funció es crida periòdicament (cada READ_PERIOD) quan el mode Reading està activat en l'Animator (sempre) i
    //serveix per a modificar l'angle dels motors del frame actual.
    //La funció ha de retornar un array de 2 ints omplert amb els nous angles dels motors.
    //El primer int correspon a l'angle del primer motor.
    //El segon int correspon a l'angle del segon motor.
    public static int[] readMode(){
        int [] exemple = new int [2];
        exemple[0] = 45;
        exemple[1] = 63;

        System.out.println("S'acaba d'executar una actualització dels motors de l'Animator amb els següents valors:");
        System.out.println("Motor1 = " + exemple[0]);
        System.out.println("Motor2 = " + exemple[1]);
        return exemple;
    }
}
