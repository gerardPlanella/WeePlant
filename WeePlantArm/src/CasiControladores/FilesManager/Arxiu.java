package CasiControladores.FilesManager;

import org.json.JSONObject;

/**
 * Arxiu es la classe contenedora dels arxius Json. Aquesta classe apart de guardar el contingut,
 * guarda altre informacio com per exemple si el fitxer té un format correcte.
 */

public class Arxiu {

    /** Nom del arxiu complet (amb .json)*/
    private String nom;

    /** Si el format es correcte, guarda el contingut del fitxer. De lo contrari, val null*/
    private JSONObject jsonObject;

    /** La quantitat de Bytes que ocupa el arxiu*/
    private long capacitat;

    /** Nombre de caracters del json*/
    private int nombreCaracters;

    /** Nombre de linies del json*/
    private int nombreLinies;

    /**
     * Crea un nou arxiu amb un nom, contingut format json i una capacitat.
     * En cas de no tenir un format correcte, l'arxiu guarda el JSONObject com null.
     * @param nom nom del nou arxiu json
     * @param jsonObject contingut en format json
     * @param capacitat nombre de bytes que ocupa l'arxiu
     */

    public Arxiu(String nom, JSONObject jsonObject, long capacitat){
        this.nom = nom;
        this.jsonObject = jsonObject ;
        this.capacitat = capacitat;
    }


    /**Getters i Setters de Arxiu*/
    public void setEstadistiques(int nombreCaracters, int nombreLinies){
        this.nombreCaracters = nombreCaracters;
        this.nombreLinies = nombreLinies;
    }

    public String getNombreCaracters() {
        return nombreCaracters + "";
    }

    public String getNombreLinies() {
        return nombreLinies + "";
    }

    public String getNom() {
        return nom;
    }

    public String getContingut(){
        return jsonObject.toString(4);
    }
    public JSONObject getJsonObject(){
        return jsonObject;
    }

    /**
     * Es important redefinir el metode toString,
     * ja que es el String usat al render de la JList per visualitzar l'element.
     * @return retorna el text que es mostrara en el JList.
     */

    @Override
    public String toString(){
        return nom + " - " + capacitat + " Bytes";
    }

}
