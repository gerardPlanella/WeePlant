package CasiControladores;

import CasiControladores.FilesManager.Arxiu;
import CasiControladores.FilesManager.ArxiuManager;
import CasiControladores.FilesManager.MalformedJsonFileException;
import Model.RobotFrame;

import Vistas.FinderWindow;
import Vistas.WeePlantArm_3D_View;
import org.json.JSONArray;
import org.json.JSONObject;

import javax.swing.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.event.MouseInputListener;
import java.awt.event.*;
import java.io.IOException;
import java.util.LinkedList;

import static java.lang.Thread.sleep;

public class AnimatorController implements ActionListener, ChangeListener, MouseInputListener,Runnable,KeyListener {

    ;
    private double animationSpeed;
    private static Animator animator;
    private ArxiuManager manager;

    private FinderWindow finder;

    private int actualFrame;
    private LinkedList<RobotFrame> frames;

    private static RobotFrame actualRobotFrame;

    private boolean animationRunning;
    private long lastSend = 0;

    public AnimatorController(Animator animator, FinderWindow fw) {
        AnimatorController.animator = animator;
        finder = fw;

        frames = new LinkedList<>();
        for(int i = 0; i < 2;i ++) frames.add(new RobotFrame());
        animator.representaFrame(frames.get(actualFrame));

        manager = new ArxiuManager();
        Thread a = new Thread(this);
        a.start();
        ExitManager.addThread(a);
        animationSpeed = 1;
    }



    @Override
    public void actionPerformed(ActionEvent e) {

        switch (e.getActionCommand()){
            case "startAnimation":
                animationRunning = true;
                break;
            case "updateFrameRate":

                String text = animator.getUpdateRate();
                if(text.isEmpty()) {
                    finder.showDialog("Error setting animation fps",
                            "Expected a positive double number",
                            "error");
                    animationSpeed = 0.0f;
                }else animationSpeed = Double.valueOf(text);

                break;
            case "stopAnimation":
                animationRunning = false;
                break;
            case "restartAnimation":
                animationRunning = false;
                actualFrame = 0;
                animator.representaFrame(frames.get(actualFrame));
                animator.updateSlider(actualFrame);
                break;
            case "Interpolate":
                interpolate(0);

                animator.updateDuracioTotal(frames.size());
                break;
            case "saveAnimation":
                saveAnimation();
                break;
            case "loadAnimation":
                animationRunning = false;
                finder.setVisible(true);
                updateJSONList();
                break;
            case "moreFrames":
                frames.add(new RobotFrame());
                animator.updateDuracioTotal(frames.size());
                break;
            case "lessFrames":
                if(frames.size() > 1){
                    frames.removeLast();
                    animator.updateDuracioTotal(frames.size());
                }
                break;
            //El boto actualitzar s'ha premut
            case "Actualitzar":

                //Es refresca la llista d'animacions
                updateJSONList();
                break;

            //El boto carregar s'ha premut
            case "Carregar":
                //Es carrega l'arxiu selecionat al animador
                carregar();
                break;
        }
        animator.focusCanvas();
    }

    private void interpolate(int interpolationPoints){
        LinkedList<LinkedList<RobotFrame>> listOfNewFrames = new LinkedList<>();
        int size = frames.size();
        int interpolationValue = (interpolationPoints == 0 ? animator.getInterpolationPoints() : interpolationPoints);

        for(int i = 0; i < size; i++){
            if(i + 1 == size) break;
            listOfNewFrames.add(interpolateTwoFrames(frames.get(i), frames.get(i+1), interpolationValue));
        }

        int index = 1;
        for (LinkedList<RobotFrame> newFrames : listOfNewFrames) {

            for (RobotFrame rf : newFrames) {
                frames.add(index++, rf);
            }
            //Salta el frame que li hem pasat a interpolate.
            index++;
        }
    }

    private LinkedList<RobotFrame> interpolateTwoFrames(RobotFrame robotFrame, RobotFrame robotFrame1, int steps) {
        LinkedList<RobotFrame> robotFrames = new LinkedList<>();

        int base_i = robotFrame.getValues()[1];
        int base_f = robotFrame1.getValues()[1];

        int arm_i = robotFrame.getValues()[0];
        int arm_f = robotFrame1.getValues()[0];

        int arm1_i = robotFrame.getValues()[2];
        int arm1_f = robotFrame1.getValues()[2];

        int arm2_i = robotFrame.getValues()[3];
        int arm2_f = robotFrame1.getValues()[3];

        float inc_base = (float)(base_f - base_i) / (float)(steps+1);
        float inc_arm  = (float)(arm_f  - arm_i)  / (float)(steps+1);
        float inc_arm1 = (float)(arm1_f - arm1_i) / (float)(steps+1);
        float inc_arm2 = (float)(arm2_f - arm2_i) / (float)(steps+1);

        float angle_base = (float)base_i;
        float angle_arm  = (float)arm_i;
        float angle_arm1 = (float)arm1_i;
        float angle_arm2 = (float)arm2_i;

        int iterations = 0;
        do {
            angle_base += inc_base;
            angle_arm  += inc_arm;
            angle_arm1 += inc_arm1;
            angle_arm2 += inc_arm2;

            iterations++;

            RobotFrame frame = new RobotFrame((int)angle_arm, (int)angle_base, (int)angle_arm1, (int)angle_arm2);
            robotFrames.add(frame);
        }while(iterations < steps);

        return robotFrames;
    }

    private void nextFrame() {
        actualFrame ++;
        if(actualFrame >= frames.size()) actualFrame = frames.size() - 1;
        //if(actualFrame >= frames.size()) actualFrame = 0;
        animator.representaFrame(frames.get(actualFrame));
        animator.updateSlider(actualFrame);
    }

    private void prevFrame() {
        actualFrame --;
        if(actualFrame < 0) actualFrame = frames.size() - 1;
        animator.representaFrame(frames.get(actualFrame));
        animator.updateSlider(actualFrame);
    }

    private void updateJSONList(){
        //Es refresca la llista del LSFinder
        manager.clearArxiuList();
        buscarArxiusJson();
    }

    @Override
    public void stateChanged(ChangeEvent e) {

        JSlider slider = (JSlider) e.getSource();
        if(slider.getValueIsAdjusting()) {
            actualFrame = slider.getValue();
            animator.representaFrame(frames.get(actualFrame));
            animator.updateSlider(actualFrame);
            animator.focusCanvas();
        }
    }

    @Override
    public void mouseClicked(MouseEvent e) {

    }

    @Override
    public void mousePressed(MouseEvent e) {
        animator.mousePress(true);
    }

    @Override
    public void mouseReleased(MouseEvent e) {
        animator.mousePress(false);
    }

    @Override
    public void mouseEntered(MouseEvent e) {}

    @Override
    public void mouseExited(MouseEvent e) {}

    @Override
    public void mouseDragged(MouseEvent e) {
        updateMouse(e);
    }

    @Override
    public void mouseMoved(MouseEvent e) {
        updateMouse(e);
    }

    private void updateMouse(MouseEvent e){
        if(animator.mouseMoved(e.getX(),e.getY())){
            if(System.currentTimeMillis() - lastSend >= Estudiant.WRITE_PERIOD){
                lastSend = System.currentTimeMillis();
            }
        }
    }

    /**
     * buscarArxiusJson busca tots els arxius en format .json de la carpeta data.
     * Un cop troba un arxiu, el guarda. En cas de detectar que l'arxiu té un format json erroni,
     * guarda l'arxiu indicant que aquest es corrupte/erroni.
     */

    private void buscarArxiusJson(){

        StringBuilder errors = new StringBuilder();
        boolean error = false;
        int numberErrors = 0;

        //Va buscant arxius fins a trobar-ne tots. En cas de trobar un d'incorrecte, salta l'excepcio MalformedJsonFileException
        do {
            try {
                manager.lookForJsonFiles();
            } catch (MalformedJsonFileException e) {
                error = true;
                errors.append(e.getArxiu().getNom());
                errors.append(System.lineSeparator());
                numberErrors++;
                manager.addArxiu(e.getArxiu());
            }

        }while(!manager.estanElsArxiusCarregats());

        if(error){

            if(numberErrors > 1)
                //S'indica al usuari amb un error que el arxiu json trobat conté un error o varis errors
                finder.showDialog("Error en la recerca d'arxius .json",
                        "S'han trobat " + numberErrors + " fitxers amb errors:\n" + errors.toString(),
                        "error");
            else
                //S'indica al usuari amb un error que el arxiu json trobat conté un error o varis errors
                finder.showDialog("Error en la recerca d'arxius .json",
                        "S'ha trobat un fitxer amb errors:\n" + errors.toString(),
                        "error");
        }

        //Amb el seguent codi es refresca la llista d'arxius del LSFinder
        finder.resetList();
        for(Arxiu arxiu : manager.getArxius()){
            finder.addToList(arxiu);
        }
    }

    private void saveAnimation() {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("{");
        stringBuilder.append("\"totalFrames\":");
        stringBuilder.append("\"").append(frames.size()).append("\",");

        stringBuilder.append("\"duracioTotal\":");
        stringBuilder.append("\"").append(animationSpeed).append("\",");

        int size = frames.size();
        stringBuilder.append("\"keyFrames\":[");
        for(int i = 0; i < size; i++) stringBuilder.append(frames.get(i).toJSON(i == size - 1));
        stringBuilder.append("]}");

        System.out.println("JSON is " + stringBuilder.toString());
        try {
            if (animator.getFileName().length() == 0){
               finder.showDialog("No name file","FileName has to be 1+ char long","error");
            }else{
                manager.createFile(animator.getFileName().contains(".json") ? animator.getFileName() : animator.getFileName() + ".json",stringBuilder.toString());
            }
        } catch (IOException | MalformedJsonFileException e) {
            e.printStackTrace();
        }
    }

    /**
     * Gestiona la funcio del boto carregar de LSFinder.
     */

    private void carregar(){

        //En el cas de haver selecionat un arxiu i que aquest sigui correcte, el carreguem a LSParser
        if (!finder.isSelectionEmpty() && finder.getSelecio().getJsonObject() != null) {

            manager.setArxiuSelecionat(finder.getSelecio());

            JSONObject novaAnimacio = manager.getArxiuSelecionat().getJsonObject();

            double tempsDeAnimacio = Double.valueOf((String)novaAnimacio.get("duracioTotal"));
            int totalNumberOfFrames = Integer.valueOf((String)novaAnimacio.get("totalFrames"));

            JSONArray newFramesData = novaAnimacio.getJSONArray("keyFrames");
            frames.clear();

            int[] buffer = new int[4];

            for(int iFrame = 0; iFrame < totalNumberOfFrames; iFrame++){

                JSONObject newFrameJSON = ((JSONObject) newFramesData.get(iFrame));

                for (int motor = 0; motor < buffer.length; motor++) {
                    buffer[motor] = Integer.parseInt((String) newFrameJSON.get(motor + ""));
                }

                frames.add(new RobotFrame(buffer));
            }

            actualFrame = 0;
            animator.updateDuracioTotal(totalNumberOfFrames);

            animationSpeed = tempsDeAnimacio;
            animator.representaFrame(frames.get(actualFrame));

            finder.setVisible(false);

        }else if(finder.isSelectionEmpty()){
            //S'indica al usuari amb un error que el arxiu redactat a la textArea conté errors
            finder.showDialog("Informacio",
                    "Per a poder carregar un arxiu, has de selecionar-lo",
                    "info");
        }
    }

    @Override
    public void run() {
        try {
            while(true) {
                if (animationRunning) {
                    nextFrame();
                    sleep((long)(1000.0 / animationSpeed));
                } else {
                    sleep(1000);
                }
            }
        } catch (InterruptedException e) {
            System.out.println("Closing AnimatorController thread...");
        }
    }

    public void keyTyped(KeyEvent e) {}

    public void keyPressed(KeyEvent e) {}

    public void keyReleased(KeyEvent e) {
        switch (e.getKeyCode()){
            case KeyEvent.VK_W:
                //Live mode

                break;
            case KeyEvent.VK_DELETE:
            case KeyEvent.VK_BACK_SPACE:
                //New frame
                frames.set(actualFrame, new RobotFrame());
                animator.representaFrame(frames.get(actualFrame));
                break;
            case KeyEvent.VK_C:
                if(actualFrame == 0){
                    frames.set(actualFrame, RobotFrame.copy(frames.get(frames.size() - 1)));
                }else{
                    frames.set(actualFrame, RobotFrame.copy(frames.get(actualFrame - 1)));
                }
                animator.representaFrame(frames.get(actualFrame));

                break;

            case KeyEvent.VK_LEFT:
                prevFrame();
                break;

            case KeyEvent.VK_RIGHT:
                nextFrame();
                break;
        }
    }

    public static void updateMotors(int motor1, int motor2, int motor3, int motor4) {

        animator.getActualFrame().updateValue(motor1,0);
        animator.getActualFrame().updateValue(motor2,1);
        animator.getActualFrame().updateValue(motor3,2);
        animator.getActualFrame().updateValue(motor4,3);
    }

    public void updateMotors(String[] d) throws InterruptedException {
        int [] newValues = {Integer.parseInt(d[2]), Integer.parseInt(d[5]), Integer.parseInt(d[3]),Integer.parseInt(d[4])};

        RobotFrame lastFrame = frames.get(actualFrame);
        animator.representaFrame(lastFrame);

        frames.clear();
        frames.add(lastFrame);
        frames.add(new RobotFrame(newValues));

        if(Integer.parseInt(d[6]) == 1){
            WeePlantArm_3D_View.pickTool(WeePlantArm_3D_View.TOOL.WATER_TOOL);
        }else if(Integer.parseInt(d[6]) == 2){
            WeePlantArm_3D_View.pickTool(WeePlantArm_3D_View.TOOL.SOIL_TOOL);
        }else if(Integer.parseInt(d[6]) == 3){
            WeePlantArm_3D_View.pickTool(WeePlantArm_3D_View.TOOL.NONE);
        }

        interpolate(Integer.parseInt(d[1]));

        actualFrame = 0;
        animationSpeed = Integer.parseInt(d[0]);
        animator.updateDuracioTotal(frames.size());
        animationRunning = true;

        while(actualFrame != frames.size() - 1){
            sleep(100);
        }

    }
}