package Vistas;

import CasiControladores.*;

import processing.core.PApplet;
import processing.core.PShape;
import processing.event.MouseEvent;

import static java.awt.event.KeyEvent.VK_CONTROL;
import static java.awt.event.KeyEvent.VK_SPACE;

public class WeePlantArm_3D_View extends PApplet{

    private PShape terra, base, hombro, pot;
    private PShape one,two,three;
    private float rotX, rotY;
    private static float pitch_hombro;
    private static float yaw;
    private static float pitch_colze;
    private static float pitch_endeffector;

    private static TOOL toolSelected;
    private static float zoom;
    private static boolean []showPot = {false ,false, false};

    public static void addPot(int potToAdd) {
        if(potToAdd == 0){
            showPot = new boolean[]{false, false, false};
            return;
        }
        showPot[potToAdd - 1] = true;
    }

    public enum TOOL{
        WATER_TOOL,
        SOIL_TOOL,
        NONE
    }

    public static void main(String[] args) {
        pitch_hombro = 3 * PI / 2;
        yaw = PI / 2;
        pitch_colze = 3 * PI / 2;
        pitch_endeffector = PI / 2;
        toolSelected = TOOL.NONE;
        zoom = 1;
        PApplet.main("Vistas.WeePlantArm_3D_View");
    }

    public void settings(){
        size(600, 663, P3D);
    }

    public void setup(){

        String folder = "robot_parts/";

        base = loadShape(folder + "r1.obj");
        hombro = loadShape(folder + "r2.obj");
        terra = loadShape(folder + "r3.obj");
        pot = loadShape(folder + "pot.obj");


        one = loadShape(folder + "1.obj");
        two = loadShape(folder + "2.obj");
        three = loadShape(folder + "3.obj");

        one.disableStyle();
        two.disableStyle();
        three.disableStyle();

        base.disableStyle();
        pot.disableStyle();
        hombro.disableStyle();
        terra.disableStyle();
    }

    public void draw(){
        if (frameCount == 1) {
            mainSecundari();
        }

        background(33);
        noStroke();

        smooth();
        lights();
        directionalLight(100, 100, 100, 1, 10, 1);

        translate(width / 2.0f,height / 1.30f);

        rotateX(rotX + PI);
        rotateY(rotY);

        scale(zoom);


        pushMatrix();

        rectMode(CENTER);
        rotateX(PI/2);
        fill(50, 50, 50);
        rect(0,0,1000,1000);

        popMatrix();

        float rad = terra.getWidth()/1.5f;
        int potNum = 0;
        for(float angle = 0; angle < 360; angle++) {
            if((angle == 30) || (angle == 60) || (angle == 90)) {
                if((showPot[0] && angle == 30) || (showPot[1] && angle == 60)  || (showPot[2] && angle == 90) ){
                    //Draw number
                    pushMatrix();
                    scale(8);
                    translate( cos((float)Math.toRadians(angle)) * (rad/1.5f), 0,sin((float)Math.toRadians(angle)) * (rad/1.5f));
                    rotateY(PI);
                    rotateX(PI/2);

                    fill(255,255,255);

                    if(potNum == 0)
                        shape(one);
                    else if(potNum == 1)
                        shape(two);
                    else if(potNum == 2)
                        shape(three);
                    popMatrix();


                    fill(226, 183, 105);
                    //Draw pot
                    pushMatrix();
                    scale(3);
                    translate( cos((float)Math.toRadians(angle)) * rad, 0,sin((float)Math.toRadians(angle)) * rad);
                    shape(pot);
                    popMatrix();
                }
                potNum++;

            }else if(angle == 270 && toolSelected != TOOL.WATER_TOOL){
                pushMatrix();
                fill(30,144,255);
                translate( cos((float)Math.toRadians(angle)) * (rad + 30), 0,sin((float)Math.toRadians(angle)) * (rad + 30));
                drawCylinder(10, 0, 20, 4);
                popMatrix();
            }else if(angle == 200 && toolSelected != TOOL.SOIL_TOOL){
                pushMatrix();
                fill(160,82,45);
                translate( cos((float)Math.toRadians(angle)) * (rad + 30), 0,sin((float)Math.toRadians(angle)) * (rad + 30));
                drawCylinder(10, 0, 20, 4);
                popMatrix();
            }
        }

        //Color del robot
        fill(35,32,32);
        translate(0,terra.getHeight(),0);
        shape(terra);

        fill(35,32,32);
        translate(0, 4, 0);
        rotateY(yaw + PI / 2);
        shape(base);

        fill(255,115,21);
        translate(0, 25, 0);
        rotateY(PI);
        rotateX(-pitch_hombro + PI);
        shape(hombro);

        fill(255,115,21);
        translate(0, 0, 50);
        rotateY(PI);
        rotateX(pitch_colze);
        shape(hombro);


        translate(0, 0, 50);
        rotateX(pitch_endeffector + PI);
        noStroke();

        if(toolSelected == TOOL.WATER_TOOL){
            fill(30,144,255);
        }else if(toolSelected == TOOL.SOIL_TOOL){
            fill(160,82,45);
        }

        if(toolSelected != TOOL.NONE) {
            drawCylinder(10, 0, 20, 30);
        }
    }

    public void keyPressed(){
        if(key == 'a'){
            pickTool(TOOL.SOIL_TOOL);
        }else if(key == 's'){
            pickTool(TOOL.WATER_TOOL);
        }else{
            pickTool(TOOL.NONE);
        }
    }

    public static void pickTool(TOOL newTool){
        toolSelected = newTool;
    }

    public void mouseDragged(){
        rotY -= (mouseX - pmouseX) * 0.005;
        rotX -= (mouseY - pmouseY) * 0.005;
    }

    public void mouseWheel(MouseEvent event){
        zoom -= event.getCount() * 0.05f;
        if(zoom <= 0) zoom = 0;
    }

    private void mainSecundari(){
        surface.setLocation(641,0);

        ExitManager.init();

        FinderWindow fw = new FinderWindow();

        Animator animator = new Animator(0);
        AnimatorController ac = new AnimatorController(animator, fw);

        //Haha q lleig
        new Reciever(ac);

        animator.addController(ac);
        fw.configController(ac);

        animator.setVisible(true);

        Thread a = new Thread(animator);
        a.start();
        ExitManager.addThread(a);
    }

    public static void updateYaw(float newYaw){
        yaw = newYaw;
    }

    public static void updatePitchHombro(float newPitch){
        pitch_hombro = newPitch;
    }
    public static void updatePitchColze(float newYaw){
        pitch_colze = newYaw;
    }

    public static void updatePitchEndEffector(float newPitch) {
        pitch_endeffector = newPitch;
    }

    private void drawCylinder(float topRadius, float bottomRadius, float tall, int sides) {
        float angle = 0;
        float angleIncrement = TWO_PI / sides;
        beginShape(QUAD_STRIP);
        for (int i = 0; i < sides + 1; ++i) {
            vertex(topRadius*cos(angle), 0, topRadius*sin(angle));
            vertex(bottomRadius*cos(angle), tall, bottomRadius*sin(angle));
            angle += angleIncrement;
        }
        endShape();

        // If it is not a cone, draw the circular top cap
        if (topRadius != 0) {
            angle = 0;
            beginShape(TRIANGLE_FAN);

            // Center point
            vertex(0, 0, 0);
            for (int i = 0; i < sides + 1; i++) {
                vertex(topRadius * cos(angle), 0, topRadius * sin(angle));
                angle += angleIncrement;
            }
            endShape();
        }

        // If it is not a cone, draw the circular bottom cap
        if (bottomRadius != 0) {
            angle = 0;
            beginShape(TRIANGLE_FAN);

            // Center point
            vertex(0, tall, 0);
            for (int i = 0; i < sides + 1; i++) {
                vertex(bottomRadius * cos(angle), tall, bottomRadius * sin(angle));
                angle += angleIncrement;
            }
            endShape();
        }
    }
}
