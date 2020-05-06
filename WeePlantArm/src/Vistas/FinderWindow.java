package Vistas;


import CasiControladores.FilesManager.Arxiu;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;


public class FinderWindow extends JFrame {

    /** Boto per actualitzar la llista d'arxius*/
    private JButton actualitzarButton;

    /** Boto per carregar l'arxiu seleccionat*/
    private JButton carregarButton;

    /** Model de la llista*/
    private DefaultListModel<Arxiu> listModel;

    /** Llista d'arxius*/
    private JList jList;

    /**
     * Es construeix tot el JFrame
     */

    public FinderWindow(){
        //S'inicialitza la llista (buida)
        listModel = new DefaultListModel<>();
        jList = new JList<>(listModel);

        //Es fa una variacio del cellRender de la JList per obtindre uns millors resultats d'UI
        jList.setCellRenderer(new auxCellRender(new DefaultListCellRenderer()));

        //Es configura la llista per cumplir amb l'enunciat
        jList.setSelectionMode(ListSelectionModel.SINGLE_INTERVAL_SELECTION);
        jList.setLayoutOrientation(JList.VERTICAL);
        jList.setVisibleRowCount(-1);
        jList.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));

        getContentPane().add(new JScrollPane(jList),BorderLayout.CENTER);


        //Es crea el panell inferior on es trobaran els dos botons
        JPanel jPanelInferior = new JPanel();

        jPanelInferior.setBorder(BorderFactory.createEmptyBorder(5, 10, 5, 10));

        //Es crean els boton i s'afegeixen al panell
        actualitzarButton = new JButton("Update");
        carregarButton = new JButton("Load");

        jPanelInferior.add(actualitzarButton);

        //S'utilitza un separador per aconseguir un 'look' mes acertat
        jPanelInferior.add(Box.createRigidArea(new Dimension(5, 0)));
        jPanelInferior.add(carregarButton);

        getContentPane().add(jPanelInferior,BorderLayout.SOUTH);

        //Configuracio basica del JFrame
        setMinimumSize(new Dimension(50,150));
        pack();

        //Centrem la finestra en el centre de la pantalla
        setLocationRelativeTo(null);
        setTitle("Animation Finder");
        setResizable(false);
        setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
    }

    /**
     * configController serveix per a establir el controlador per a cada component de la UI.
     * @param controlador La classe que gestionará la interacció del usuari amb els arxius de /data.
     */

    public void configController(ActionListener controlador){

        //S'afegeixen tots els action listeners al contingut interactuable.
        actualitzarButton.addActionListener(controlador);
        carregarButton.addActionListener(controlador);

        actualitzarButton.setActionCommand("Actualitzar");
        carregarButton.setActionCommand("Carregar");
    }

    /**
     * Borra tots els elements de la llista
     */

    public void resetList(){
        listModel.removeAllElements();
    }

    /**
     * Afegeix un arxiu a la llista
     * @param newArxiu arxiu que es vol afegir
     */

    public void addToList(Arxiu newArxiu){
        listModel.addElement(newArxiu);
        pack();
    }

    /**
     * Genera un diaeg per notificar al usuari sobre informacio o un error.
     * @param title Titol de obtindra el dialeg.
     * @param missatge Missatge intern del dialeg.
     * @param type Tipus de dialeg.
     */

    public void showDialog(String title,String missatge,String type) {
        if(type.equalsIgnoreCase("error"))
            JOptionPane.showMessageDialog(this,missatge,title,JOptionPane.ERROR_MESSAGE);
        else
            JOptionPane.showMessageDialog(this,missatge,title,JOptionPane.INFORMATION_MESSAGE);
    }

    /**Getters i setters*/

    public boolean isSelectionEmpty(){
        return jList.isSelectionEmpty();
    }
    public Arxiu getSelecio(){
        return (Arxiu)jList.getSelectedValue();
    }

}