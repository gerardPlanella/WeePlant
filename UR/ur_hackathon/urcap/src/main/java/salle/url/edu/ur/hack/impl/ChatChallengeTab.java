package salle.url.edu.ur.hack.impl;

import javax.swing.*;
import java.awt.*;
/**Prova afegir imatge*/

public class ChatChallengeTab extends JPanel {

    public ChatChallengeTab() {

        this.setAlignmentX(Component.LEFT_ALIGNMENT);

        JPanel jpParent = new JPanel();

        JTextArea jtaExplicacio = new JTextArea(
                "RECONOCIMIENTO DE VOZ\n" +
                "\n" +
                "Para poder interactuar con el robot, se dispone de la aplicación desarrollada para iphones o ipads llamada URApp. En ella, se puede acceder al chatbot donde se pueden realizar las siguientes acciones mediante el control por voz:\n" +
                "    * Crear o cargar un programa\n" +
                "    * Mover el robot\n" +
                "        - Mediante el modo libre, donde podemos mover el robot libremente\n" +
                "        - Mediante comandos para moverlo arriba/abajo/derecha/izquierda/delante/atrás\n" +
                "        - Mediante comandos para moverlo a través de los ejes X/Y/Z\n" +
                "    * Poner en funcionamiento un programa, ponerlo en pausa y pararlo\n" +
                "    * Pedir información al robot\n" +
                "        - Temperatura de cada articulación\n" +
                "        - Voltage de cada motor\n" +
                "        - Corriente de cada motor\n" +
                "    * Aviso de colisión, parada de emergencia...\n" +
                "    * Crear una pequeña charla con el robot");

        jtaExplicacio.setSize(800,600);
        jtaExplicacio.setLineWrap(true);
        jtaExplicacio.setWrapStyleWord(true);
        jtaExplicacio.setAutoscrolls(true);

        jpParent.add(jtaExplicacio);

        this.add(jpParent);

    }

}
