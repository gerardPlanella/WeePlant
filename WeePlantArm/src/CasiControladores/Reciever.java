package CasiControladores;

import com.sun.org.apache.xalan.internal.xsltc.trax.OutputSettings;
import jdk.internal.util.xml.impl.Input;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

public class Reciever extends Thread {
    private final static int PORT = 25852;
    private ServerSocket serverSocket;

    private final AnimatorController animatorController;

    public Reciever(AnimatorController ac){
        ExitManager.addThread(this);

        animatorController = ac;

        serverSocket = null;
        try {
            serverSocket = new ServerSocket(PORT);
            this.start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void run() {


        while (true){
            Socket cs = null;
            BufferedReader reader;
            OutputStreamWriter writer;
            try {
                cs = serverSocket.accept();

                reader = new BufferedReader(new InputStreamReader( cs.getInputStream()));
                writer = new OutputStreamWriter(cs.getOutputStream(), StandardCharsets.UTF_8);

            } catch (IOException e) {
                e.printStackTrace();
                return;
            }

            System.out.println("Client connected to WeePlantRobot");
            while(true) {
                try {
                    String data = reader.readLine();
                    if (data != null) {
                        System.out.println("Rebut: " + data);
                        String[] d = data.split("[.]");
                        System.out.println("Rebut " + d.length);

                        //Blocking untill it reaches the goal!s
                        animatorController.updateMotors(d);
                        writer.append("Vamos!");
                        writer.flush();

                    }else {
                        break;
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                    break;
                }
            }
            try {
                cs.close();
                System.out.println("Connection closed");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
