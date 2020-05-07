package CasiControladores;

import com.fazecast.jSerialComm.SerialPort;

import javax.swing.*;
import java.util.LinkedList;

public class ExitManager {

    private static LinkedList<JFrame> frames;
    private static LinkedList<Thread> threads;
    private static LinkedList<SerialPort> ports;

    public static void init(){
        frames = new LinkedList<>();
        threads = new LinkedList<>();
        ports = new LinkedList<>();
    }

    public static void addThread(Thread newTh){
        threads.add(newTh);
    }
    public static void addJFrame(JFrame newJF){
        frames.add(newJF);
    }

    public static void exit(){

        System.out.println("Tencant recursos...");

        for(SerialPort p : ports){
            if(!p.closePort()){
                System.out.println("Error tencant el port " + p.getPortDescription());
            }
        }

        for(Thread t : threads){
            t.interrupt();
        }

        for(JFrame f : frames){
            f.dispose();
        }

        System.exit(0);
    }

    public static void removePort(SerialPort port) {
        ports.remove(port);
    }

    public static void addPort(SerialPort port) {
        ports.add(port);
    }
}
