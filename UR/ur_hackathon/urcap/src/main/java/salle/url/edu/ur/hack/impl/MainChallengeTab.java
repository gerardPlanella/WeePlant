package salle.url.edu.ur.hack.impl;

import javax.swing.*;
import java.awt.*;

public class MainChallengeTab extends JPanel {

    public MainChallengeTab() {

        this.setAlignmentX(Component.LEFT_ALIGNMENT);

        JPanel jpParent = new JPanel();
        jpParent.setLayout(new BoxLayout(jpParent, BoxLayout.Y_AXIS));

        JLabel jtaExplicacio = new JLabel(
                "Bienvenidos a HackTheCobot\n");
        jtaExplicacio.setFont(jtaExplicacio.getFont().deriveFont(48.0f));
        JLabel empty = new JLabel(
                "\n");
        jpParent.add(empty);
        jpParent.add(jtaExplicacio);

        //Prova afegir imatge
        //Cargar imatge
        ImageIcon iiImatge = new javax.swing.ImageIcon(getClass().getResource("/laSalle.jpg"));
        //TODO: util per a escalar la imatge Crear imatge
        Image iImatge = iiImatge.getImage();
        //Crear jLabel per a posar-ho a dins
        JLabel jlImatge = new JLabel();
        jlImatge.setIcon(iiImatge);
        jlImatge.setSize(402,176);
        //Afegir imatge al jpParent
        jpParent.add(jlImatge);

        this.add(jpParent);

    }

}
