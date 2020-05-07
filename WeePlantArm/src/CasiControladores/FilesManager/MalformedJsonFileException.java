package CasiControladores.FilesManager;

import org.json.JSONException;

/**
 * Excepcio adicional necesaria per a poder definir Arxius json corruptes o malformats.
 * Facilita la causa del problema i l'arxiu on s'ha trobat l'incident, ja creat en forma corrupte.
 * Pertant l'arxiu que es guarda en l'excepcio sap que es corrupte o erroni.
 */

public class MalformedJsonFileException extends Exception {
    private Arxiu arxiu;
    private String motiu;

    public MalformedJsonFileException(JSONException e, Arxiu arxiu){
        super("Arxiu mal format!");
        motiu = e.getLocalizedMessage();
        this.arxiu = arxiu;
    }

    public Arxiu getArxiu() {
        return arxiu;
    }

    public String getMotiu() {
        return motiu;
    }

}
