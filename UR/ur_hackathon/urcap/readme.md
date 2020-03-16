# Com crear la URCAP amb IntelliJ

(només compilar-la, no es veu la interfície)

1. Descarregar SDKs que trobareu al loggar-vos al següent enllaç:
    1.1 https://www.universal-robots.com/plus/developer/login/
    1.2 ATENCIÓ!!!! Tarden fins a un màxim de 2 dies en donar-vos accés!
2. Obrir la carpeta "urcap" a l'IntelliJ.
3. Afegir les SDKs a l'IntelliJ. Per a fer-ho:
    3.1 File --> Project Structure...
    3.2 A sota de "Platform Settings", trobem "SDKs". Presionem aquí i ens ha de sortir totes les SDKs que hi ha actualment al projecte.
    3.3 Per a afegir-ne una altra, donar-li al botonet '+' de la dreta. S'obrirà una finestreta on us permetrà seleccionar les SDKs que voleu (podeu seleccionar més d'una a la vegada si presioneu la tecla 'ctrl')
    3.4 Polsar el botó 'Apply' i 'OK'

4. Compilar el projecte
	4.1 Per a compilar el projecte, fer click amb el botó dret del ratolí a sobre de la carpeta "urcap" i seleccionar "Build module "ur-hack"".
	4.2 Un cop hagi fet el build, s'ha de donar-li al run. Per a fer-ho, fer click altre cop amb el boto dret a "urcap" i seleccionar Run 'All Tests'

5. Obtenció del fitxer .jar
	5.1 El fitxer el trobarem a urcap/target/ur-hack-1.0-SNAPSHOT.jar

6. Si per algun motiu es vol modificar el codi, el trobareu a:
urcap/src/main/java/salle.url.edu.ur.hack.impl
	6.1 ChatChallengeTab es on hi ha l'explicacio de speech
	6.2 ARChallengeTab es on hi ha l'explicacio de AR
	6.3 DataChallengeTab es on hi ha explicacio DASHBOARD & VISUALIZACIÓN 3D
	6.4 El nom de les pestanyetes el trobareu a LsInstallationNodeView

# Posar el fitxer al robot
Atenció, en un principi, el codi que està penjat, ja és capaç de fer les modificacions pertinents i enviar el fitxer al robot. Tot i això, s'explica com s'ha de fer.

1. Un cop obtenim el fitxer .jar, se li ha de canviar per .urcap. És a dir, passar de ur-hack-1.0-SNAPSHOT.jar a ur-hack-1.0-SNAPSHOT.urcap
2. Obrir el terminal del robot ('Ctrl'+'Alt'+'F1' o qualsevol altre fins a 'F6')
2.1 Usuari: root Contrassenya: easybot
3. Copiar el programa .urcap a programs/
3.1 Si el teniu en un pen, simplement heu de fer el següent:
```sh
cd /media
cd /urmountpoint_v08bQn (o algun nom raro similar)
cp ./ur-hack-1.0-SNAPSHOT.urcap /programs
```