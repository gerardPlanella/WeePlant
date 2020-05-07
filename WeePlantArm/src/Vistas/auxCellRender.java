package Vistas;

import CasiControladores.FilesManager.Arxiu;

import javax.swing.*;
import java.awt.*;

/**
 * Implementacio del Render que utilitza el JList per a mostrar cada casella de la llista.
 * Aquesta implementacio em permet indicar a la Llista el meu propi Render.
 * Aixo provoca que es puguin pintar les caselles de la llista segons criteris marcats per mi.
 */

public class auxCellRender extends JLabel implements ListCellRenderer {

    /**
     * Aquesta variable em facilita la implementacio del render.
     * Me la facilita perque ella mateixa ja implementa al render.
     * Pertant puc estar tranquil de modificar el render, que no he determinar tots
     * els parametres especificats amb el LookAndFeel predeterminat de la JList.
     */

    private DefaultListCellRenderer defListCellRender;

    /** Crea el render i guarda el default render*/

    public auxCellRender(DefaultListCellRenderer defaultListCellRenderer) {
        setOpaque(true);
        defListCellRender = defaultListCellRenderer;
    }


    /**
     * D'aquesta implementacio es interesant observar l'us comentat anteriorment del default render.
     * Es pot observar com getListCellRendererComponent retorna el component que apareixera en el JList
     * visualment per a cada casella.
     * Es per aixo que amb aquesta classe em permet inserir-me en la meitat del proces,
     * de manera que abans de retornar el component es pot modificar a gust de personal
     * nomes aquelles qualitats que es necesiten. Sense sobrescriure completament el lookAndFeel original.
     */

    @Override
    public Component getListCellRendererComponent(JList list, Object value, int index, boolean isSelected, boolean cellHasFocus) {


        Component c = defListCellRender.getListCellRendererComponent( list, value, index, isSelected, cellHasFocus );

        //Com es sap que value es un object del tipus de la Llista, podem tractar-lo com un arxiu
        Arxiu arxiu = (Arxiu) value;

        //En el cas de no ser un arxiu json correcte, es pinta a la llista amb un background vermell
        if(arxiu.getJsonObject() != null){

            if(!isSelected)
                c.setBackground(new Color(0.0f,1.0f,0.0f,0.3f));
            else
                c.setBackground(new Color(0.0f,1.0f,0.0f,0.7f));
        }else{

            //Sino es pinta verd
            if(!isSelected)
                c.setBackground(new Color(1.0f,0.0f,0.0f,0.3f));
            else
                c.setBackground(new Color(1.0f,0.0f,0.0f,0.7f));
        }

        return c;
    }
}
