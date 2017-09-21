======================================================
 KRONOS ISMS - Information Security Management System
======================================================

Einleitung
----------
Diese Applikation soll eine Datenbasis liefern, die als Grundlage für das ISMS
bei **KRONOS** verwendet werden kann. In erster iteration soll dies vor allem 
eine CMDB sein die im Anschluss um weitere, wichtige Infromationen, wie
beispielsweise die zugrhörigen Prozesse einschließler der Relevanz im hinblick
auf Datenschutz, ergänzt wird. 


Vorgehen
--------
Eine CMDB von Grund auf neu zu erstellen macht keinen Sinn, weil viele
Informationen bereits irgendwo gespeichert sind. Ziel ist es daher, diese
Informationen zu sammeln und einheitlich aufzubereiten. Hierfür werden zunächst
folgende System in Betracht gezogen:

1) Active Directory
    - Computer (Server/Clients)
    - Netzkomponenten
    - Lokationen
    - Anwender
    - Client-Applikationen (über Altiris Gruppen)
    - Drucker
2) Altiris
    - Computer (Server/Clients)
    - Lokationen
    - Client-Applikationen
    - Zuordnung Client - Anwender
3) Lotus Notes
    - Anwender
    - Meetingräume
    - Parkplätze
    - Prozesse (TQM)
4) Check_MK Monitoring
    - Computer (Server)
    - Service
    - Datenbank
    - Drucker

Und weitere Systeme kommen noch in Betracht:
- Qualys
- LogRhythm
- TK-Anlage
- McAfee
- vCenter
