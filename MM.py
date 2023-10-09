"""

This module/program was partly generated by artificial intelligence. The AI used is/was ChatGPT from openAI available at https://chat.openai.com/


Doc


Data Storage:
data_store = DataStore("subfolder", "File.json")  # Initializing the class
subfolder: the folder where data is stored
File.json: the name of the file to store data, always in JSON format

data_store.save("key", value)  # Saves data
value = data_store.load("key")  # Loads data

key: identifier for the respective value
value: data to be stored


Logging:
logger = Log(number_of_logs)  # Initialization
number_of_logs: default is 5 log files

logger.info("message")
logger.warning("message")
logger.error("message")
logger.debug("message")

message: the log message


User Input Handling:
input_handler = Input()  # Initialization
integer = input_handler.int("prompt_message")
floating_point = input_handler.float("prompt_message")

Returns user input as the respective data type.


Sorting:
sorted_list = Sorting(integer_list).sort()
integer_list: a list of integers


Package Manager:
package_manager = PackageManager()  # Initialization

package_manager.install_module("module")
module: the name of the module to be installed via pip


Secure Encryption:
secure_encryptor = SecE("encryption_key")  # Initialization
encryption_key: the password

encrypted_data = secure_encryptor.encrypt("original_data")
decrypted_data = secure_encryptor.decrypt("encrypted_data")

encrypted_data: the encrypted dataset
decrypted_data: the decrypted dataset
original_data: the original dataset


"""

import base64
import hashlib
import os
import json
import logging
import concurrent.futures
import glob
from datetime import datetime


class SSD:
    def __init__(self, ordner="DATA", dateiname="DATA"):
        self.ordner = ordner
        self.dateiname = dateiname
        self.pfad = os.path.join(ordner, dateiname)
        self.daten = {}
        self.daten_laden()

    def save(self, schluessel, wert):
        self.daten[schluessel] = wert
        self.daten_speichern()

    def daten_laden(self):
        try:
            with open(self.pfad, 'r') as datei:
                inhalt = datei.read()
                if inhalt:
                    self.daten = json.loads(inhalt)
        except FileNotFoundError:
            # Wenn die Datei nicht gefunden wird, erstelle eine leere Datenstruktur
            self.daten = {}

    def load(self, schluessel=None):
        if schluessel:
            return self.daten.get(schluessel, None)
        return self.daten

    def daten_speichern(self):
        os.makedirs(self.ordner, exist_ok=True)
        with open(self.pfad, 'w') as datei:
            json.dump(self.daten, datei, indent=2)


class log:
    def __init__(self,  log_count=5 ,log_dir='logs' , log_level=logging.DEBUG):
        self.log_dir = log_dir
        self.log_count = log_count-1

        # Stelle sicher, dass das Verzeichnis existiert, falls nicht, erstelle es
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Lösche ältere Log-Dateien, wenn die Anzahl überschritten wird
        self.cleanup_logs()

        # Setze den Dateinamen basierend auf der Startzeit
        log_file = os.path.join(self.log_dir, f"{datetime.now().strftime('%Y%m%d%H%M%S')}.log")

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # Erstelle einen Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # Erstelle einen Handler zum Schreiben von Log-Nachrichten in die Datei
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        # Füge den Handler zum Logger hinzu
        self.logger.addHandler(file_handler)

    def cleanup_logs(self):
        # Holen Sie alle Log-Dateien im Verzeichnis
        log_files = glob.glob(os.path.join(self.log_dir, '*.log'))
        # Sortiere sie nach Änderungsdatum (neueste zuerst)
        log_files.sort(key=os.path.getmtime, reverse=True)

        # Behalte nur die neuesten log_count Dateien
        if len(log_files) > (self.log_count):
            for old_log_file in log_files[self.log_count:]:
                os.remove(old_log_file)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)



class Input:
    def __init__(self):
        self.integer_input = None
        self.float_input = None

    def int(self, msg="Bitte geben Sie eine Ganzzahl ein: "):
        try:
            self.integer_input = int(input(msg))
            return self.integer_input
        except ValueError:
            print("Ungültige Eingabe. Bitte geben Sie eine Ganzzahl ein.")
            return self.int()

    def float(self, msg="Bitte geben Sie eine Gleitkommazahl ein: "):
        try:
            self.float_input = float(input(msg))
            return self.float_input
        except ValueError:
            print("Ungültige Eingabe. Bitte geben Sie eine Gleitkommazahl ein.")
            return self.float()


class Sorting:
    def __init__(self, array):
        self.array = array

    def sort(self):
        if len(self.array) <= 10:  # Optimierter Basisfall für kleine Arrays
            return sorted(self.array)

        num_threads = min(2, len(self.array))  # Anzahl der Threads anpassen

        if len(self.array) < 10000:  # Anpassen der Schwelle für die Entscheidung
            return self.quick_sort()
        else:
            mid = len(self.array) // 2
            left_half = self.array[:mid]
            right_half = self.array[mid:]

            # Verwenden Sie ThreadPoolExecutor für parallele Ausführung
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                # Starten Sie die Ausführung der Teilaufgaben
                future1 = executor.submit(Sorting(left_half).sort)
                future2 = executor.submit(Sorting(right_half).sort)

                # Warten Sie auf das Ende der Teilaufgaben und erhalten Sie die Ergebnisse
                result1 = future1.result()
                result2 = future2.result()

            # Kombinieren Sie die Ergebnisse
            return self.merge(result1, result2)

    def quick_sort(self):
        if len(self.array) <= 1:
            return self.array
        else:
            pivot = self.array.pop()
            less_than_pivot = [x for x in self.array if x <= pivot]
            greater_than_pivot = [x for x in self.array if x > pivot]

            return Sorting(less_than_pivot).quick_sort() + [pivot] + Sorting(greater_than_pivot).quick_sort()

    def merge(self, left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result


class PackageManager:
    def __init__(self):
        pass
    def install_module(self, module_name):
        try:
            # Überprüfe, ob das Modul bereits installiert ist
            if not self.is_module_installed(module_name):
                os.system(f"pip install {module_name}")
                return True
            else:
                return True
        except:
            return False

    def is_module_installed(self, module_name):
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False

class SecE:
    def __init__(self, key):
        pm = PackageManager()
        pm.install_module("cryptography")
        del pm
        from cryptography.fernet import Fernet
        self.key = hashlib.sha256(key.encode()).digest()
        self.cipher_suite = Fernet(base64.urlsafe_b64encode(self.key))

    def encrypt(self, data):
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data.decode()

    def decrypt(self, encrypted_data):
        try:
            decrypted_data = self.cipher_suite.decrypt(encrypted_data.encode())
            return decrypted_data.decode()
        except:
            return False

