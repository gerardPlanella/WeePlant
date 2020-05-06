package Model;

public class RobotFrame {

    private int[] values;

    public RobotFrame(int ... frames){
        values = new int[4];

        for(int i = 0 ;i < values.length; i++){
            int[] initFrameAngle = {90, 90, 90, 90};
            if(i < frames.length) values[i] = frames[i];
            else values[i] = initFrameAngle[i];
        }
    }

    public static RobotFrame copy(RobotFrame frame) {
        return new RobotFrame(frame.getValues());
    }

    public int[] getValues() {
        return values;
    }

    @Override
    public String toString() {
        StringBuilder aux = new StringBuilder();
        aux.append("[ ");
        for(int v : values){
            aux.append(" ").append(v);
        }
        aux.append(" ]");
        return aux.toString();
    }

    public String toJSON(boolean last) {
        StringBuilder aux = new StringBuilder("{");
        for(int i= 0; i < values.length; i++){
            aux.append("\"").append(i).append("\":").append("\"").append(values[i]);
            if(i == values.length-1) aux.append("\"");
            else aux.append("\",");
        }
        aux.append("}");
        if(!last) aux.append(",");
        return aux.toString();
    }

    public void updateValue(int newVal, int index){
        values[index] = newVal;
    }
}