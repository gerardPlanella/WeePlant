package salle.url.edu.ur.hack.impl;

import javax.swing.*;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import java.awt.*;

public class D3ChallengeTab extends JPanel {

    public D3ChallengeTab() {
        this.setAlignmentX(Component.LEFT_ALIGNMENT);

        JPanel jpParent = new JPanel();

        JTextArea jtaExplicacio = new JTextArea("" +
                "VISUALIZACIÓN 3D\n" +
                "\n" +
                "Para acceder a la información del robot, se dispone de una applicación de escritorio llamada UR Remote Desktop. En ella se puede acceder a todos los robots que hay en la empresa pudiendo realizar las siguientes acciones:\n" +
                "    * Acceder a información del robot en tiempo real como:\n" +
                "        - Temperatura de cada articulación\n" +
                "        - Voltage de cada motor\n" +
                "        - Corriente de cada motor\n" +
                "        - Velocidad de la articulación en radianes\n" +
                "        - Estado de la articulación\n" +
                "    * Visualización global de la temperatura de cada articulación mediante una escalera de colores\n" +
                "    * Ver los movimientos en tiempo real del robot\n" +
                "    * Ver las paredes que estan actualmente activadas\n" +
                "    * Mostrar distinitas alertas del robot\n" +
                "    * Controlar los angulos de las distintas articulaciones mediante el teclado o arrastrando el ratón\n" +
                "    * Pedirle al robot que vaya a un determinado punto configurado\n" +
                "    * Pedirle al robot que ejecute un determinado programa guardado en el robot\n" +
                "    * Pedirle al robot que baile");

        jtaExplicacio.setSize(800,600);
        jtaExplicacio.setLineWrap(true);
        jtaExplicacio.setWrapStyleWord(true);
        jtaExplicacio.setAutoscrolls(true);

        jpParent.add(jtaExplicacio);

        this.add(jpParent);
    }

}
