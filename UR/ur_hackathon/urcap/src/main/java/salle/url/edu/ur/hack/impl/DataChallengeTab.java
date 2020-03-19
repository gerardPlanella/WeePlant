package salle.url.edu.ur.hack.impl;

import javax.swing.*;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import java.awt.*;

public class DataChallengeTab extends JPanel {

    public DataChallengeTab() {
        this.setAlignmentX(Component.LEFT_ALIGNMENT);

        JPanel jpParent = new JPanel();

        JTextArea jtaExplicacio = new JTextArea("" +
                "DASHBOARD\n" +
                "\n" +
                "El dashboard permite visualizar de manera fácil y cómoda tanto datos generales respecto a la producción de una fábrica, como datos específicos respecto al estado de un robot concreto.\n" +
                "\n" +
                "Panel general:\n" +
                "Detalla información referente a:\n" +
                "    * La producción de la fábrica (número de ciclos finalizados, tiempo por ciclo, etc.)\n" +
                "    * Ranking de robots y trabajadores\n" +
                "    * Información referente a pérdidas de unidades de productos\n" +
                "\n" +
                "Panel planta:\n" +
                "Permite la visualización global de la planta de la fábrica. Se muestra:\n" +
                "    * Valores generales de la planta\n" +
                "    * El estado de los robots usando una codificación basada en colores\n" +
                "    * Datos concretos de un robot\n" +
                "\n" +
                "Paneles trabajadores y robots:\n" +
                "Lista los trabajadores y robots de la fábrica. Una vez aquí, se puede acceder al detalle de cada uno.\n" +
                "En el caso de los robots, podemos ver:\n" +
                "    * Información genérica, estado y tarea actual\n" +
                "    * Histórico del funcionamiento del robot\n" +
                "    * Información a tiempo real de los motores\n" +
                "    * Notificaciones del robot y visualizarlas todas las que se han produido en formato tabla");

        jtaExplicacio.setSize(800,600);
        jtaExplicacio.setLineWrap(true);
        jtaExplicacio.setWrapStyleWord(true);
        jtaExplicacio.setAutoscrolls(true);

        jpParent.add(jtaExplicacio);

        this.add(jpParent);
    }

}
