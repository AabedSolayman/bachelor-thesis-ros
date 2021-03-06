# -*- coding: utf-8 -*-
# Quellcode GATT-Client-Klasse. Der GATT-Client kann ein Windows-PC oder Raspberry sein.  
# Über diesen Client wird der MoveHub gesteuert bzw. dessen Sensorwerte ausgelesen.
# Für den BlueGiga BLE-Dongle BLED112 wird hierfür von der Bibliothek pygatt das BGAPIBackend
# verwendet. Für das interne BLE-Interface des Raspberry Pi wird die Bibliothek gatt-python (gatt)
# verwendet, die auf Linux BlueZ basiert. 
# Somit ist dieser Code sowohl auf Windows-PCs (mit BlueGiga Dongle) als auch für Linuxrechner
# (mit und ohne Dongle) lauffähig.
# Wichtig ist beim BlueGiga-Dongle, dass dieser beim Start mit der Bibliothek pygatt nicht
# resettet wird. Sonst gibtes (nur?) auf der Ubuntu 18.04 Plattform Laufzeitfehler.
# Siehe Methode BLEClient.conn_bluegiga().
#
# S. Mack, 21.3.2020

"""
Dieses Package kuemmert sich um die Kommunikation zwischen MoveHub (GATT-Server und einem
externem Rechner (GATT-Client). Fuer den BlueGiga BLED112 Dongle wird Linux und Windows
unterstuetzt. Zusaetzlich wird BlueZ unter Linux (Raspberry Pi 3) unterstuetzt.
"""

import sys
import pygatt # lokales pygatt verwenden
import logging
from time import sleep
from pygatt.backends.bgapi.util import find_usb_serial_devices
from pylegoboost import constants as C
from pylegoboost.utilities import str2hex
if sys.platform.startswith('linux'): # gatt gibt es nur fuer Linux. Nur dann importieren
    import gatt
    import threading

BLED112_VENDOR_ID = 0x2458
BLED112_PRODUCT_ID = 0x0001

class BLEClient():
    """
    Herstellung der BLE-Vebindung zwischen MoveHub und Client.
    Erkennen des BlueGiga BLED112 Dongels und Verwendeung als
    bevorzugtes BLE-Interface im Modus "Auto". Ohne BlueGiga-Dongle
    nur Verbindung mit Linux-GATT-Client via BlueZ.
    """
    #ble_iface=None

    def __init__(self,backend='Auto',controller='hci0',hub_mac=''):
        if backend in ['Auto', 'BlueZ', 'BlueGiga']:
            self.system = sys.platform
            print('Erkanntes Betriebssystem: ', self.system)
            if self.system.startswith('linux'):
                self.system = 'linux'
            if self.system in ['linux', 'win32']:
                detected_ifaces = find_usb_serial_devices(vendor_id=BLED112_VENDOR_ID,product_id=BLED112_PRODUCT_ID)
                if backend == 'Auto':                   
                    if self.system == 'linux': # Linux-Betriebssystem, Praesenz BlueGiga Dongle pruefen:
                        if len(detected_ifaces) == 0: # BlueGiga nicht gefunden, also verwende BlueZ
                            print('Kein BlueGiga-Dongle unter Linux gefunden, verwende BlueZ-Interface.')
                            self.controller = controller
                            self.conn_bluez(hub_mac,controller)
                        else: # BlueGiga gefunden und diesen verwenden
                            self.controller=detected_ifaces[0].port_name
                            print('BlueGiga-Dongle unter Linux gefunden unter: ', self.controller)
                            self.conn_bluegiga(hub_mac)                   
                    else: # Windows-Betriebssystem
                        if len(detected_ifaces) == 0:
                            print('Kein BlueGiga-Dongle unter Windows gefunden > Programmabbruch')
                        else:
                            self.controller=detected_ifaces[0].port_name
                            print('BlueGiga-Dongle unter Windows gefunden unter: ', self.controller)                            
                            self.conn_bluegiga(hub_mac)
                elif backend == 'BlueZ':
                    self.controller = controller
                    self.backend = backend
                    self.conn_bluez(hub_mac,controller)
                elif backend == 'BlueGiga':
                    self.controller = controller
                    self.backend = backend
                    self.conn_bluegiga(hub_mac)
            else:
                print('Betriebssystem {} wird nicht unterstützt'.format(sys.platform))
        else:
            print('Ungültige BLE-Interface Option, muss entweder BlueZ (linux), BlueGiga (linux oder Windows) oder Auto sein.')
            sys.exit(0)
        
    def conn_bluez(self,hub_mac,controller): # Mit internem BLE-Interface verbinden (nur Linux)      
        self.backend = 'BlueZ'
        # vor Instanzierung muss DeviceManger gestartet sein
        logging.debug('BlueZ: DeviceManager Instanz erzeugen...')
        dev_manager = gatt.DeviceManager(adapter_name=controller)
        dman_thread = threading.Thread(target=dev_manager.run)
        logging.debug('BlueZ: DeviceManager starten...')
        dman_thread.start()
        #sleep(1)
        self.ble_iface=BlueZInterface(hub_mac,controller,dev_manager,dman_thread)
        print('BlueZ-Interface gestartet. Bitte MoveHub einschalten!')
        self.ble_iface.client_conn(hub_mac)
        print('BlueZ-Interface unter Linux verbunden.')
        
    def conn_bluegiga(self,hub_mac): # Mit BLE-Interface ueber BlueGiga-Dongle verbinden (Linux und Windows)
        self.backend = 'BlueGiga'
        self.ble_iface = BlueGigaInterface()
        try:
            self.ble_iface.start(reset=False) # BLE-Interface zuruecksetzen, kein Dongle-Reset, sonst Laufzeitfehler
            print('BlueGiga-Interface gestartet. Bitte MoveHub einschalten!')
        except:
            print('Start des BlueGiga-Interfaces fehlgeschlagen!')
        sleep(1) 
        self.ble_iface.client_conn(hub_mac)
        print('BlueGiga-Interface unter Linux bzw. Windows verbunden.')    
    
    def disconnect(self):
        self.ble_iface.stop()
        print('BLE-Verbindung mit MoveHub beendet, BLE-Interface wurde getrennt.')    
        
    def online(self): # Methode zur Kontrolle ob Verbindung besteht oder nicht
        if (self.ble_iface != None):
            return self.ble_iface.online() # Verbindung erfolgreich und BlueZ Device Manager laeuft
            logging.info('BlueGiga: BLE-Client online')
            #return True
        else:
            return False # Falls keine Instanz existiert, dann auch keine Verbindung
            logging.info('BlueGiga: BLE-Client offline')
            #return False

      
if sys.platform.startswith('linux'): # (python-)gatt gibt es nur fuer Linux - nur dann Klassen erstellen
        
    class BlueZInterface(gatt.Device): # Pendant zu Klasse BlueGigaInterface
        """
        Integriertes BLE-Interface auf Linuxrechner wie Raspberry Pi, 
        welches ueber BlueZ betrieben wird.
        """
        def __init__(self, mac_address, controller, manager,dman_thread):
            logging.debug('BlueZ: Interface Instanz erzeugen...')
            super().__init__(mac_address=mac_address, manager=manager)
            self.conn_hnd_char = None # BLE-Verbindungs-Handle Kommunikation fuer Characteristic Handle 0x0e  
            #self.not_func=None # Callbackfunktion, die bei Notifications ausgefuehrt werden soll
            self.manager=manager
            self.dman_thread=dman_thread
                       
        def start(self): # Dummy, da DeviceManager vor Instanzierung gestartet werden musste
            pass
        
        def client_conn(self,hub_mac): # Client mit dem GATT-Server MoveHub (MAC-Adresse hub_mac) verbinden
            logging.debug("BlueZ: Trying to connect client to MoveHub with MAC %s.", hub_mac)
            self.connect() # Kann unterschiedlich lang dauern, daher Warteschleife
            logging.debug('Warte auf services.resolved()...')
            #sleep(1)
            while self.conn_hnd_char == None: # ErhÃ¤lt erst Wert, wenn richtige Characterisitc gefunden
                sleep(0.1)
                print('*',end='')
            print('')
            logging.debug('services.resolved() erfolgreich')

        def read(self,handle):  # Lesen Charakteristic ueber Handle (noch nicht implementiert!!)
            print('Achtung: BlueZ gatt read command (dummy!)')
            logging.debug("BlueZ: Reading from handle %s. Dummy!!!", handle)
            return b'\0x00\0x00'
            
        def write(self,handle,data): # Schreiben an Charakteristic 0x0e
            logging.debug("BlueZ: Writing to handle 0x0e: %s", str2hex(data))
            return self.conn_hnd_char.write_value(data) 
            
        def enable_notifications(self): # Notifications aktivieren
            logging.debug('BlueZ: Enable Notifications...')
            #sleep(0.5)
            self.conn_hnd_char.enable_notifications()
            #sleep(1)        

        def set_notific_handler(self,uuid,func_hnd): # Callbackfunktion fuer Notifications festlegen
            logging.debug('BlueZ: set_notific_handler()')
            self.not_func=func_hnd
        
        def stop(self): # Verbindung trennen
            logging.debug('Stopp DeviceManager anschliessend BLE-Verbindung trennen')
            self.manager.stop()
            sleep(2)
            self.disconnect()

        def online(self): # Kontrolle ob der Device Manager noch lebt und Verbindung stattgefunden hat
            logging.info('BlueZ.online()')
            if self.dman_thread:
                if self.conn_hnd_char != None:
                    return self.dman_thread.isAlive()
                    logging.info('BlueZ: BLE-Client online')
            else:
                return False
                logging.info('BlueZ: BLE-Client offline')

        #------------------------------------------------------------------
        # Ab hier Event-Methoden der Elternklasse, die ueberschrieben werden
        def services_resolved(self): # Wird automatisch bei connect() ausgefuehrt
            logging.debug('MoveHub Services und Characteristics ermitteln...')
            super().services_resolved()
            logging.debug("[%s] Resolved services",self.mac_address)
            for service in self.services: # Suche nach 0x0e Charakteristic fuer MoveHub-Steuerung
                logging.debug("[%s]  Service [%s]",self.mac_address, service.uuid)
                for characteristic in service.characteristics:
                    logging.debug("[%s]    Characteristic [%s]" ,self.mac_address, characteristic.uuid)
                    if (service.uuid == C.MOVE_HUB_HW_UUID_SERV and
                        characteristic.uuid == C.MOVE_HUB_HW_UUID_CHAR):
                        logging.debug('MoveHub Charakteristik gefunden!')
                        self.conn_hnd_char = characteristic # nicht besser bekannte Char. fest zuweisen?
            if self.conn_hnd_char==None: # Programmabbruch, falls Characteristic 0x0e nicht gefunden
                print('BlueZ hat Characteristic fÃ¼r MoveHub Steuerung nicht gefunden! > Programmabbruch.')
                self.stop()
                sleep(1)
                sys.exit(0)

        # Callback Funktion fuer Notifications. Angabe des Handle nicht noetig,
        # da nur fuer eine Characteristic Notifications abonniert wurden
        def characteristic_value_updated(self, characteristic, value):
            logging.debug('Notification in GattDevice: %s',value.hex())
            self.not_func(handle=0x0e,data=value) # Anders als beim BlueGiga generell nur Notifications von 0x0e      

        def connect_succeeded(self): # Nur zum Debuggen bei Problemen innerhalb gatt noetig.
            super().connect_succeeded()
            logging.debug('gatt.Device: Erfolgreich verbunden')

        def connect_failed(self, error): # Nur zum Debuggen bei Problemen innerhalb gatt noetig.
            super().connect_failed(error)
            print("Verbindung fehlgeschlagen:", str(error))
            self.manager.stop()
            
        def disconnect_succeeded(self): # Nur zum Debuggen bei Problemen innerhalb gatt noetig.
            super().disconnect_succeeded()
            logging.debug('gatt Bibliothek meldet Ende BLE-Verbindung.')
        #------------------------------------------------------------------


class BlueGigaInterface(pygatt.BGAPIBackend): # Pendant zu Klasse BlueZInterface
    """
    Durch BlueGiga BLED112 Dongle bereitgestelltes externes BLE-Interface auf Linux-
    oder Windowsrechnern.
    """
    def __init__(self): # ZusÃ¤tzliches Attribut conn_hnd = Handle auf BLE-Verbindung
        pygatt.BGAPIBackend.__init__(self)
        self.conn_hnd=None # Handle BLE-Verbindung = Rueckgabeobjekt Funktion connect() anders als BlueZInterface!!

    def client_conn(self,hub_mac): # Client mit dem GATT-Server MoveHub (MAC-Adresse hub_mac) verbinden
        logging.debug("BlueGiga: Trying to connect client to MoveHub with MAC %s.", hub_mac)
        self.conn_hnd=self.connect(hub_mac)

    def read(self,handle): # Lesen Charakteristik ueber angegebenes Handle
        logging.debug("BlueGiga: Reading from handle %s.", handle)
        return self.conn_hnd.char_read_handle(handle)
        
    def write(self,handle,data): # Schreiben Charakteristik ueber angegebenes Handle
        logging.debug("BlueGiga: Writing to handle %s: %s", handle, str2hex(data))
        return self.conn_hnd.char_write_handle(handle,data) 
        
    def set_notific_handler(self,uuid,func_hnd): # Callbackfunktion fuer Notifications festlegen
        logging.debug("BlueGiga: Set notification handler to callback function.")
        self.conn_hnd.subscribe(uuid, func_hnd)

    def enable_notifications(self):
        self.write(C.ENABLE_NOTIFICATIONS_HANDLE, C.ENABLE_NOTIFICATIONS_VALUE)

    def online(self): # Kontrolle, ob Verbindungsprozess stattgefunden hat
        if self.conn_hnd==None:
            return False
        else:
            return True
               
    # Verbindung trennen mit Aufruf BLECleint.ble_iface.stop() bewirkt 
    # pygatt.BGAPIBackend.stop(). Daher hier nicht implementiert.
