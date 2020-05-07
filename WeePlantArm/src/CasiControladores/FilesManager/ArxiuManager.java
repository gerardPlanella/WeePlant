package CasiControladores.FilesManager;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.*;
import java.util.ArrayList;

/**
 * Arxiu manager s'encarrega de gestionar i guardar tots els arxius del sistema.
 * Es capaç de buscar i crear json respectant el format.
 */

public class ArxiuManager {

    /** Llista de arxius carregats al sistema desde la carpeta AnimationsSaved*/
    private ArrayList<Arxiu> arxius;

    /** Indica si tot el contingut de la carpeta AnimationsSaved ha sigut processat*/
    private boolean totCarregat;

    /** Indica l'index de l'ultim arxiu que s'ha processat en el sistema*/
    private int indexUltimArxiuMalformat;

    /** Arxiu que esta actualment tractant LSParser*/
    private Arxiu arxiuSelecionat;

    /** Crea el model del sistema*/
    public ArxiuManager(){
        arxius = new ArrayList<>();
        totCarregat = false;
        indexUltimArxiuMalformat = 0;
    }

    /**
     * lookForJsonFiles esta dedicada a la actualització dels arxius que guarda el Model.
     * Aquesta funcio busca i actualitza els arxius.json de la carpeta AnimationsSaved.
     * En cas de trobar un error, ho notifica i indica quin arxiu de la llista conté un problema.
     * @throws MalformedJsonFileException En cas de detectar un error en el format del JSON alhora de crear el JSONObject,
     * s'utilitza aquesta Exception per crear un arxiu definit com malformat.
     */

    public void lookForJsonFiles() throws MalformedJsonFileException {

        //S'obre la carpeta AnimationsSaved i la guardem en un file
        File f =  new File("AnimationsSaved");

        //S'obte una llista del arxius de AnimationsSaved
        File [] files = f.listFiles();

        //En cas de tenir arxius a AnimationsSaved els processem
        if(files != null) {

            //La iteracio s'inicia a indexUltimArxiuMalformat perque en cas de trobar un arxiu malformat,
            //saltara una excepcio per guardar el arxiu en questio de forma especial.
            //Un cop guardar, s'actualitza indexUltimArxiuMalformat i es torna a cridar aquesta funcio.
            for (int i = indexUltimArxiuMalformat; i < files.length; i++) {

                File arxiu  = files[i];

                if(arxiu.getName().substring(arxiu.getName().indexOf(".") + 1).equals("json")) {

                    try {
                        //Intentem afegir l'arxiu
                        arxius.add(new Arxiu(arxiu.getName(),fileToJSONObject(arxiu),arxiu.length()));
                    }catch (JSONException e){
                        //Format incorrecte, guardem l'index per quan es torni a aquesta funcio posteriorment.
                        indexUltimArxiuMalformat = ++i;
                        throw new MalformedJsonFileException(e,new Arxiu(arxiu.getName(),null,arxiu.length()));
                    }catch (IOException e){
                        //En cas de no existir el file (cosa molt poc probable) ho indiquem per consola.
                        System.out.println("En el temps de llegir el .json, algu ha borrat el " + arxiu.getName());
                    }
                }
            }
            //Un cop aconseguim transpasar el bucle, significa que tots els arxius estan carregats.
            totCarregat = true;
        }
    }

    /**
     * fileToJSONObject converteix un file a un JSONObject.
     * En cas de trobar qualsevol problema, aquest es tracta en la funcio que ha solicitat fer la conversio.
     * @param f arxiu que es vol convertir.
     * @return JSON contingut al arxiu f.
     * @throws JSONException En cas de detectar un error en el format del JSON alhora de crear el JSONObject.
     * @throws IOException En cas de no existir el file.
     */

    private JSONObject fileToJSONObject(File f) throws JSONException,IOException {


        //Pasem el arxiu a convertir dins el BufferedReader
        BufferedReader br = new BufferedReader(new FileReader("AnimationsSaved/" + f.getName()));
        StringBuilder sb = new StringBuilder();

        //Es llegeixen totes les linies del BufferedReader
        String line = br.readLine();
        while (line != null) {
            sb.append(line);
            sb.append(System.lineSeparator());
            line = br.readLine();
        }

        //Es crea un JSONObject amb el string generat per la suma de les linies
        return new JSONObject(sb.toString());
    }

    /**
     * Reinicia completament el Model.
     * D'aquesta manera es poden tornar a llegir nous arxius.
     */

    public void clearArxiuList(){
        indexUltimArxiuMalformat = 0;
        totCarregat = false;
        arxius.clear();
    }

    /**
     * Crea un fitxer amb els continguts del JTextArea en la vista LSParser.
     * El nom del fitxer es directament el text introduit al JTextField de la mateixa vista.
     * @param textFieldContent Es el nom del nou arxiu que es vol generar.
     * @param newContent contingut que s'afegira al nou arxiu
     * @throws IOException En cas de sorgir un error amb la escriptura del propi fitxer,
     * salta la excepcio i el model s'encarrega d'advertir al usuari.
     * @throws MalformedJsonFileException Si el fitxer que es vol guardar te un format incorrecte,
     * salta la excepcio i el model s'encarrega d'advertir al usuari.
     */

    public void createFile(String textFieldContent,String newContent) throws IOException,MalformedJsonFileException{

        try (FileWriter file = new FileWriter("AnimationsSaved/" + textFieldContent)) {

            //Creant el JSONObject ja salta l'excepcio, pero el codi sembla mes autoExplicatiu d'aquesta forma
            JSONObject.testValidity(new JSONObject(newContent));

            //Es crea el arxiu amb un el contingut
            file.write(newContent);

        } catch (JSONException e){
            //Format incorrecte, creem un arxiu auxiliar per indicar més informacio sobre el problema al usuari
            throw new MalformedJsonFileException(e,new Arxiu(textFieldContent,null,0));
        }
    }

    /**
     * Retorna el arxiu amb el que esta treballant actualment LSParser. En cas de no tenir cap arxiu, crea un de nou buit.
     * @return El arxiu amb el que treballa LSParser
     */

    public Arxiu getArxiuSelecionat() {
        if (arxiuSelecionat == null) {
            arxiuSelecionat = new Arxiu("ArxiuAutoGenerat.json", null, 0);
        }
        return arxiuSelecionat;
    }

    /**Getters i setters*/
    public void setArxiuSelecionat(Arxiu newArxiu){
        this.arxiuSelecionat = newArxiu;
    }

    public ArrayList<Arxiu> getArxius() {
        return arxius;
    }

    public boolean estanElsArxiusCarregats(){
        return totCarregat;
    }

    public void addArxiu(Arxiu arxiu){
        arxius.add(arxiu);
    }
}
