package salle.url.edu.ur.hack.impl;

import javax.swing.*;
import java.awt.*;

public class ARChallengeTab extends JPanel {

    public ARChallengeTab() {

        this.setAlignmentX(Component.LEFT_ALIGNMENT);

        JPanel jpParent = new JPanel();

        JTextArea jtaExplicacio = new JTextArea(
                "REALIDAD AUMENTADA\n" +
                "\n" +
                "Para poder trabajar con la realidad aumentada, se dispone de la aplicación desarrollada para dispositivios iOS llamada URApp. En ella, se pueden configurar las siguientes opciones:\n" +
                "    * Agustar parámetros del robot \n" +
                "        - IP\n" +
                "        - Puerto para acceder a la información\n" +
                "        - Dirección de la web\n" +
                "        - Limites virtuales del robot\n" +
                "    \n" +
                "Para empezar a trabajar con ella, primero debemos calibrar el entorno de trabajo.\n" +
                "Existen 3 modos avanzados para visualizar información:\n" +
                "    * Visualizar los limites virtuales\n" +
                "    * Visualizar la información de las articulaciones, en tiempo real y en la posición donde se encuentran. Presionando encima de cada articulación, se puede acceder a la información del mismo:\n" +
                "        - Temperatura\n" +
                "        - Corriente\n" +
                "        - Voltage\n" +
                "        - Velocidad\n" +
                "    * Modo programación, donde se permite:\n" +
                "        - Crear puntos en la realidad virtual para que el robot se mueva a esa posición\n" +
                "        - Ver la trayectoria que ha ido siguiendo\n" +
                "        - Activar o desactivar la herramienta \n" +
                "        - Guardar el programa para reproducirlo de nuevo");

        jtaExplicacio.setSize(800,600);
        jtaExplicacio.setLineWrap(true);
        jtaExplicacio.setWrapStyleWord(true);
        jtaExplicacio.setAutoscrolls(true);

        jpParent.add(jtaExplicacio);

        this.add(jpParent);

    }

}
