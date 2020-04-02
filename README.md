# bachelor-thesis-ros
## Thesis title: Sensor-based navigation of a robot under ROS with triangulation scanner


Mein Abschlussprojekt beginnt am 23. März. Ich habe 125 Tage Zeit, sie zu beenden. 
Dieser Repo wird meine Arbeit an meiner Bachelorarbeit repräsentieren. Er ist zu Bildungszwecken und zur Weiterverfolgung meines Plans gedacht.
Nach 2 wöchigen Vorbereitungen und Einlernen zu den Themen ROS, Bluetooth LE, Lego, Robotik-Systemen habe ich diese TODO-Liste als Entwurf für mein Konzept erstellt. Diese TODO-Liste wird geändert und bearbeitet, solange ich mit der Abschlussarbeit weiterarbeite.




##### Thema 1)  Roboter Aufbau:

* Requirements für den Roboter erstellen (Pflichtenheft)
* Aufbau
* Simulation mit Hilfe von mecabricks.com (für bessere Messungen)
* URDF erstellen
* Bauideen für Boost-Roboter: https://www.dpunkt.de/material/openbooks/
* Oben auf dem Roboter ein „Beacon‟, dessen Position und Orientierung durch den Scanner einfach erkannt werden kann. Lässt sich vielleicht auch simulieren.
      
##### Thema 2) Odometry Source:

* Python Skript, um die Pose des Roboters zu publizieren.
* Die Pose kann vom lgbst Bibliothek erhalten werden. (Tilt sensor, Motor 
* Die Frage ist ob Dead Reckoning (=Koppelnavigation) überhaupt nötig ist, da ja Positionsmessung durch Scanner.
      
##### Thema 3) X2Lidar Scanner Datenverarbeiten:

* Python Skript für das Bearbeiten der Daten aus dem Topic „/scan“, um die Poistion bzw Orientation des Roboters zu erstellen.
* Publizieren der Position und Orientation in Topic „initialpose“.
			benutzen. 

##### Thema 4) tfs:

* Skript schreiben, um die tfs von Robotteile zu publizieren.

##### Thema 5) Map erstellen:

* Eine simulierte Map erstellen, für Testen
* echte Map mit Hilfe von X2Lidar sensor erstellen und 
* Map vielleicht gar nicht nötig, da Roboter ja nur eine in der Software vorgegebene Spur abfahren soll und im Raum keine Hindernisse oder Begrenzungen sind.

##### Thema 6) Path planning/Regelung:
- Buch Robotics, Vision and Control von P. Corke, Kapitel 4.2 (Download Hochschulbibliothek oder PDF über S. Mack)
- Simulink als Codeerzeuger dafür verwenden?

	
##### Thema 7) Navigation Stack 
* Alle Skripte in Navigation Stack zusammenfassen.
* reicht ein Regelungsknoten, der von einem Knoten mit der Sollspur diese Daten erhält.
* Ein knot für die Motor befehle

