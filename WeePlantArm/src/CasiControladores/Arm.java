package CasiControladores;


import Vistas.WeePlantArm_3D_View;

import java.awt.*;
import java.awt.geom.AffineTransform;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Rectangle2D;

import static CasiControladores.Animator.limitColor;

public class Arm{
    private double x,y,w,h;
    private int angle, maxAngle, minAngle;
    private Color ball,me;
    private boolean isHover;
    private boolean selected;
    private int armPos;

    public Arm(double x, double y, double w, double h, Color me, int ma, int mi, int center,int armPos){
        maxAngle = ma;
        minAngle = mi;
        this.armPos= armPos;
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.me = me;
        ball = new Color(200,50,50);
        isHover = false;
        angle = center;
        selected = false;
    }

    public void render(Graphics2D g){

        AffineTransform old = g.getTransform();

        if(minAngle != maxAngle && ((maxAngle - minAngle) != 360)) {
            //Render limit minim
            g.rotate(Math.toRadians(minAngle), x, y);
            g.setColor(limitColor);
            g.fill(new Rectangle2D.Double(x, y - 1, w, 2));
            g.setTransform(old);

            //Render limit minim
            old = g.getTransform();
            g.rotate(Math.toRadians(maxAngle), x, y);
            g.setColor(limitColor);
            g.fill(new Rectangle2D.Double(x, y - 1, w, 2));
            g.setTransform(old);
        }
        //Render posicio actual
        old = g.getTransform();
        g.rotate(Math.toRadians(angle),x,y);
        g.setColor(me);
        g.fill(new Rectangle2D.Double(x,y,w,h));
        g.setTransform(old);

    }

    public void renderKnob(Graphics2D g) {
        //Render knob
        g.setColor(getBallColor());
        g.fill(new Ellipse2D.Double(getBallX(10), getBallY(10), 10, 10));
    }

    public boolean hover(int x, int y, int i){
        isHover = onZone(x,y, (int) getBallX(i),(int)getBallY(i),i);
        if(isHover){
            ball = new Color(150,50,50);
        }else{
            ball = new Color(200,50,50);
        }
        return isHover || selected;
    }

    public Color getBallColor(){
        return ball;
    }

    public void update(int x,int y) {
        this.x = x;
        this.y = y;
    }

    private boolean onZone(int x, int y, int x1, int y1, int size){
        return Math.sqrt(Math.pow(x - x1,2) + Math.pow(y - y1,2)) <= size;
    }

    public boolean move(int x1, int y1) {
        if(selected){
            double val = Math.atan2((y1 - y), (x1 - x));

            int newAngle = (int) Math.toDegrees(val < 0 ? val + 2 * Math.PI : val);

            //Molt guarro, pero no vullperdre el temps.
            if(armPos == 1) {
                if (newAngle < minAngle) {
                    this.angle = minAngle;
                } else if (newAngle > maxAngle) {
                    this.angle = maxAngle;
                } else {
                    this.angle = newAngle;
                }
            }else {
                if (newAngle > 90 && newAngle < 180) {
                    this.angle = minAngle;
                } else if (newAngle < 90 && newAngle > 0) {
                    this.angle = maxAngle;
                } else {
                    this.angle = newAngle;
                }
            }

            update3D();
            return true;
        }
        return false;
    }

    public void mousePress(boolean state) {
        if(!state){
            if(selected){
                selected = false;
            }
        }else {
            selected = isHover;
        }
    }
    public double getBallX(int size){
        //TODO: dont work as good as expected.
        double adjustment = (angle < 180 ? -h / 2 : h / 2);
        return x + w * Math.cos(Math.toRadians(angle)) - size / 2.0 + adjustment;
    }

    public double getBallY(int size){
        return y + w * Math.sin(Math.toRadians(angle)) - size / 2.0 ;
    }

    public int getEndY() {
        return (int) (y + w * Math.sin(Math.toRadians(angle)));
    }
    public int getEndX() {
        return (int) (x + w * Math.cos(Math.toRadians(angle)));
    }
    public int getConvertedAngle()
    {
        return (angle - 180);
    }

    public void updateAngle(int angle) {
        this.angle = angle + 180;
        update3D();
    }

    private void update3D(){
        switch (armPos){
            case 0:
                WeePlantArm_3D_View.updatePitchHombro((float) Math.toRadians(this.angle));
                break;
            case 1:
                WeePlantArm_3D_View.updateYaw((float) Math.toRadians(this.angle));
                break;
            case 2:
                WeePlantArm_3D_View.updatePitchColze((float) Math.toRadians(this.angle));
                break;
            case 3:
                WeePlantArm_3D_View.updatePitchEndEffector((float) Math.toRadians(this.angle));
                break;
        }
    }

    public String getAngle() {
        return String.valueOf(angle - 180);
    }

}
