# -*- coding: utf-8 -*-
# Quellcode für die Kommunikation mti dem Lego Boost MoveHub aus github.com/undera/pylgbst adaptiert.
# Dort verwendete Bibliothek gattlib funktioniert prinzipiell nicht unter Windows und speziell nicht
# auf Raspberry Pi. Daher Kommunikation mit bluepy oder BlueGiga BLED112 Dongle mit Klasse BLEClient.
# BlueGiga Dongle läuft unter Windows UND Linux. Bluepy nutzt die integrierte BLE-Schnittstelle auf
# dem Raspberry Pi (BlueZ) und kann nur unter Linux verwendet werden.
# 
# S. Mack, 20.3.2020

import logging
import sys
from time import sleep
from struct import pack
from pylegoboost import bleclient as bc
from pylegoboost import constants as C
from pylegoboost.peripherals import Button,EncodedMotor,ColorDistanceSensor,LED,TiltSensor,Amperage,Voltage,Peripheral
from pylegoboost.utilities import str2hex, usbyte

# Wenn log nicht auskommentiert, dann jede Meldung (10 = DEBUG in Datei logDatei.log)
#logging.basicConfig(filename='logDatei.log', level=10)

class MoveHub(object):
    """
    :type client: pylegoboost.bleclient.BLEClient
    :type devices: dict[int,Peripheral]
    :type led: LED
    :type tilt_sensor: TiltSensor
    :type button: Button
    :type amperage: Amperage
    :type voltage: Voltage
    :type color_distance_sensor: pylgbst.peripherals.ColorDistanceSensor
    :type port_C: Peripheral
    :type port_D: Peripheral
    :type motor_A: EncodedMotor
    :type motor_B: EncodedMotor
    :type motor_AB: EncodedMotor
    :type motor_external: EncodedMotor
    """

    DEV_STATUS_DETACHED = 0x00
    DEV_STATUS_DEVICE = 0x01
    DEV_STATUS_GROUP = 0x02

    def __init__(self, client=None, hub_mac='00:16:53:AB:64:29'):
        if not client: # BBLE-Interface auswaehlen und client (PC bzw. Raspberry Pi) mit MoveHub verbinden
            self.client = bc.BLEClient(backend='Auto',controller='hci1',hub_mac=hub_mac)
        self.mac_addr=hub_mac
        self.info = {}
        self.devices = {} # Dictionary angeschlossene Peripherieobj. mit Schluessel gleich Portnummer

        # Attibute fÃ¼r die Peripherieobjekte
        self.button = Button(self)
        self.led = None
        self.amperage = None
        self.voltage = None
        self.motor_A = None
        self.motor_B = None
        self.motor_AB = None
        self.color_distance_sensor = None
        self.tilt_sensor = None
        self.motor_external = None
        self.port_C = None
        self.port_D = None
        
        # Initialisierungen: Callbackfunktion Notifications MoveHub, Peripherie suchen, Staus melden
        if(self.online()): self.client.ble_iface.set_notific_handler(C.MOVE_HUB_HW_UUID_CHAR,self._notify)
        if(self.online()): self._wait_for_devices()
        if(self.online()): self._report_status()

    def send(self, msg_type, payload):
        logging.info('movehub.send(): msg_type {0}, payload {1}'.format(msg_type,payload))
        cmd = pack("<B", C.PACKET_VER) + pack("<B", msg_type) + payload
        self.client.ble_iface.write(C.MOVE_HUB_HARDWARE_HANDLE, pack("<B", len(cmd) + 1) + cmd)

    # Angeschlossene Peripherie (Motoren, Sensoren) in durch enable_notifications() ausgeloesten neun
    # Notifications suchen, Port dazu identifizieren und fuer jede Peripherie Attibutobjekt instanzieren
    def _wait_for_devices(self):
        logging.debug('_wait_for_devices() start')
        self.client.ble_iface.enable_notifications()
        sleep(1)
        # Im MoveHub integrierte Peripherie muss anwesend sein, sonst Programmabbruch
        builtin_devices = ()
        for num in range(0, 60):
            builtin_devices = (self.led, self.motor_A, self.motor_B,
                               self.motor_AB, self.tilt_sensor, self.button, self.amperage, self.voltage)
            if None not in builtin_devices:
                return
            logging.debug("Waiting for builtin devices to appear: %s", builtin_devices)
            sleep(0.05)
        print('ERROR:Failed to obtain all builtin devices')
        logging.warning("Got only these devices: %s", builtin_devices)
        self.disconnect()
        sleep(2)
        sys.exit(0) # Programm beenden

    # Callbackfunktion fuer Notifications vom MoveHub
    # Im Vergleich zur urspruenglichen Bibliothek pylgbst andere Elemente von Bytearray data verwendet
    # und Variable orig entfernt.
    def _notify(self, handle, data):
        if handle != C.MOVE_HUB_HARDWARE_HANDLE:
            logging.warning("Unsupported notification handle: 0x%s", handle)
            return          
        logging.debug("_notify() Notification on %s: %s", handle, str2hex(data))
        
        msg_type = usbyte(data, 2)
        # Meldungstyp anhand des 2. Bytes identifizieren:
        if msg_type == C.MSG_PORT_INFO:
            self._handle_port_info(data)
        elif msg_type == C.MSG_PORT_STATUS:
            self._handle_port_status(data)
        elif msg_type == C.MSG_SENSOR_DATA:
            self._handle_sensor_data(data)
        elif msg_type == C.MSG_SENSOR_SUBSCRIBE_ACK:
            port = usbyte(data, 3)
            logging.debug("Sensor subscribe ack on port %s", C.PORTS[port])
            self.devices[port].finished()
        elif msg_type == C.MSG_PORT_CMD_ERROR:
            logging.warning("Command error: %s", str2hex(data[3:]))
            port = usbyte(data, 3)
            self.devices[port].finished()
        elif msg_type == C.MSG_DEVICE_SHUTDOWN:
            logging.warning("Device reported shutdown: %s", str2hex(data))
            raise KeyboardInterrupt("Device shutdown")
        elif msg_type == C.MSG_DEVICE_INFO:
            self._handle_device_info(data)
        else:
            logging.warning("Unhandled msg type 0x%x: %s", msg_type, str2hex(data))

    def _handle_device_info(self, data):
        kind = usbyte(data, 3)
        if kind == 2:
            self.button.handle_port_data(data)
        if usbyte(data, 4) == 0x06:
            self.info[kind] = data[5:]
        else:
            logging.warning("Unhandled device info: %s", str2hex(data))
            
    # Sensordaten vom Hub werden fuer die entsprechenden Peripherie in deren Queue geschrieben
    def _handle_sensor_data(self, data):
        port = usbyte(data, 3)
        if port not in self.devices:
            logging.warning("_handle_sensor_data() Notification on port with no device: %s", C.PORTS[port])
            return
        device = self.devices[port]
        device.queue_port_data(data)

    def _handle_port_status(self, data):
        port = usbyte(data, 3)
        status = usbyte(data, 4)        
        if status == C.STATUS_STARTED:
            self.devices[port].started()
        elif status == C.STATUS_FINISHED:
            self.devices[port].finished()
        elif status == C.STATUS_CONFLICT:
            logging.warning("Command conflict on port %s", C.PORTS[port])
            self.devices[port].finished()
        elif status == C.STATUS_INPROGRESS:
            logging.warning("Another command is in progress on port %s", C.PORTS[port])
            self.devices[port].finished()
        elif status == C.STATUS_INTERRUPTED:
            logging.warning("Command interrupted on port %s", C.PORTS[port])
            self.devices[port].finished()
        else:
            logging.warning("Unhandled status value: 0x%x on port %s", status, C.PORTS[port])

    def _handle_port_info(self, data):
        port = usbyte(data, 3)
        status = usbyte(data, 4)
        if status == self.DEV_STATUS_DETACHED:
            logging.info("Detached %s", self.devices[port])
            self.devices[port] = None
        elif status == self.DEV_STATUS_DEVICE or status == self.DEV_STATUS_GROUP:
            dev_type = usbyte(data, 5)
            self._attach_device(dev_type, port)
        else:
            raise ValueError("Unhandled device status: %s", status)
        self._update_field(port)
        if self.devices[port] is None:
            del self.devices[port]

    # Dictionary devices fuellen und dabei fuer die jeweilige Peripherie ein entsprechendes
    # Objekt erzeugen.
    def _attach_device(self, dev_type, port):
        if port in C.PORTS and dev_type in C.DEVICE_TYPES:
            logging.info("Attached %s on port %s", C.DEVICE_TYPES[dev_type], C.PORTS[port])
        else:
            logging.warning("Attached device 0x%x on port 0x%x", dev_type, port)
        if dev_type == C.DEV_MOTOR:
            self.devices[port] = EncodedMotor(self, port)
        elif dev_type == C.DEV_IMOTOR:
            self.motor_external = EncodedMotor(self, port)
            self.devices[port] = self.motor_external
        elif dev_type == C.DEV_DCS:
            self.color_distance_sensor = ColorDistanceSensor(self, port)
            self.devices[port] = self.color_distance_sensor
        elif dev_type == C.DEV_LED:
            self.devices[port] = LED(self, port)
        elif dev_type == C.DEV_TILT_SENSOR:
            self.devices[port] = TiltSensor(self, port)
        elif dev_type == C.DEV_AMPERAGE:
            self.devices[port] = Amperage(self, port)
        elif dev_type == C.DEV_VOLTAGE:
            self.devices[port] = Voltage(self, port)
        else:
            logging.warning("Unhandled peripheral type 0x%x on port 0x%x", dev_type, port)
            self.devices[port] = Peripheral(self, port)
    
    # Attribute fuer die Peripheriegeraete mit den entsprechenden Peripherieobjekten verknuepfen
    def _update_field(self, port):
        if port == C.PORT_A:
            self.motor_A = self.devices[port]
        elif port == C.PORT_B:
            self.motor_B = self.devices[port]
        elif port == C.PORT_AB:
            self.motor_AB = self.devices[port]
        elif port == C.PORT_C:
            self.port_C = self.devices[port]
        elif port == C.PORT_D:
            self.port_D = self.devices[port]
        elif port == C.PORT_LED:
            self.led = self.devices[port]
        elif port == C.PORT_TILT_SENSOR:
            self.tilt_sensor = self.devices[port]
        elif port == C.PORT_AMPERAGE:
            self.amperage = self.devices[port]
        elif port == C.PORT_VOLTAGE:
            self.voltage = self.devices[port]
        else:
            logging.warning("Unhandled port: %s", C.PORTS[port])

    # Verbindung zum MoveHub trennen (MoveHub Objekt wird aber nicht geloescht)
    def disconnect(self):
        self.client.disconnect()

    # Ausgabe Geraetename, Geraetehersteller, Batteriespannung
    def _report_status(self):
        logging.info('_report_status()')
        logging.info("%s by %s", self.info_get(C.INFO_DEVICE_NAME), self.info_get(C.INFO_MANUFACTURER))
        print('Gerätename: {}  Gerätehersteller: {}   MAC-Adresse: {}'.format(self.info_get(C.INFO_DEVICE_NAME).decode("utf-8"),self.info_get(C.INFO_MANUFACTURER).decode("utf-8"),self.mac_addr))
        self.__voltage = 0

        def on_voltage(value):
            self.__voltage = value

        self.voltage.subscribe(on_voltage, granularity=0)
        while not self.__voltage: # Dauert oft etwas laenger, da anfangs viele Spannungs-Notifications
            sleep(0.05)
        self.voltage.unsubscribe(on_voltage)
        print('Spannung MoveHub: {0:.0f} %'.format(self.__voltage*100)) #Statusmeldung bein Instanzieren
        logging.info("Voltage: %d%%", self.__voltage * 100)
        sleep(0.5) # Noetig, wenn direkt danach ein neuer Befehl wie z.B. Motoren ansteuern folgt.
        
    # Geraeteeigenschaften des MoveHubs aus dessem Speicher abfragen
    def info_get(self, info_type):
        self.info[info_type] = None
        self.send(C.MSG_DEVICE_INFO, pack("<B", info_type) + pack("<B", C.INFO_ACTION_GET))
        while self.info[info_type] is None:  # FIXME: will hang forever on error
            sleep(0.05)
        return self.info[info_type]
        
    # Methode zur Kontrolle ob fuer den MoveHub eine BLE-Verbindung besteht oder nicht
    # Gibt True bzw. False zurueck
    def online(self):
        logging.info('MoveHub.online()')
        return self.client.online()
        
