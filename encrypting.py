from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from pathlib import Path
import random, encrypt_ui
from math import log2 as lg2
import ca

class SecretKey(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = encrypt_ui.Ui_Dialog()
        self.fname = None
        self.cellular = None
        self.String_Bits = ""
        self.encrypted_message = ""
        self.Bits = None
        self.rules = None
        self.entropie = None
        self.ui.setupUi(self)
        self.ui.encrypt_key.clicked.connect(self.encrypt_clicked) #podlacza przycisk do funkcji
        self.ui.decrypt_key.clicked.connect(self.decrypt_clicked) #jw
        self.ui.load_image.clicked.connect(self.load_image_clicked)
        self.ui.set_seed.clicked.connect(self.load_set_seed)
        self.acceptance_threshold = float(self.ui.eat_box.currentText())
        self.cells_number = 0
        self.entropy = 0


    @pyqtSlot()
    def load_set_seed(self):
        tmp_seed = self.ui.seed_amount_box.text()
        if tmp_seed.isdecimal():
            random.seed(int(tmp_seed))

    def generate_random_rules(self, number):
        self.rules = []
        for i in range(number):
            self.rules.append(random.randrange(0, 256))

    def generate_recommended_rules(self, number):
        self.rules = []
        for i in range(number):
            val = random.randrange(0, 4)
            if val == 0:
                self.rules.append(90)
            elif val == 1:
                self.rules.append(105)
            elif val == 2:
                self.rules.append(150)
            elif val == 3:
                self.rules.append(165)

    def string2bits(self, s=''):  # zmienia text na bity
        return [bin(ord(x))[2:].zfill(8) for x in s]

    def bits2string(self, b=None):  # zamienia bity na text
        return ''.join([chr(int(x, 2)) for x in b])

    def xor(self, x1, x2):
        tmp = ""
        for n in range(len(x2)):
            if (n < len(x1)):
                if int(x2[n]) and not int(x1[n]) or int(x1[n]) and not int(x2[n]):
                    tmp += "1"
                else:
                    tmp += "0"
            else:
                tmp += x2[n]
        return tmp

    @pyqtSlot()
    def encrypt_clicked(self):
        self.encryption()

    def encryption(self): # zmienia na postac binarna jesli klucz nie jest pusty i robi XOR
        if self.ui.cells_number.text() is not "" and self.fname:

            self.String_Bits, self.bytes_number = self.file_to_bits(self.fname)

            entropia = 0
            self.acceptance_threshold = float(self.ui.eat_box.currentText())
            while entropia < self.acceptance_threshold:
                self.acceptance_threshold = float(self.ui.eat_box.currentText())
                if self.ui.radio_specified_rules.isChecked():  # tutaj wchodzi jak sa zaznacozne reguly 90, 105, 150, 165
                    self.generate_recommended_rules(int(self.ui.cells_number.text()))

                else:
                    self.generate_random_rules(int(self.ui.cells_number.text()))

                self.cellular = ca.CellularAutomaton(self.losowe_zera_i_jedynki(len(self.rules)),
                                                     non_uniform_rules=self.rules)

                length = len(self.String_Bits)
                if length < 16 * int(self.ui.h_box.currentText()):
                    length = 16 * int(self.ui.h_box.currentText())
                self.iterate_iterate(length)
                rand_index = random.randrange(0, self.cellular.automaton_length)
                self.generated_password = self.return_pseudorandom_number_sequence(rand_index)
                entropia = self.entropia(self.generated_password)
                print(self.generated_password + " " + str(entropia))

            self.entropy = entropia
            self.ui.final_entropy_box.setText(str(self.entropy))

            self.ui.text_binary.setText(self.String_Bits)
            print(len(self.String_Bits))
            self.ui.key_binary.setText(self.generated_password)
            print(len(self.generated_password))
            self.encrypted_message = self.xor(self.String_Bits, self.generated_password)
            self.ui.text_binary.setText(self.String_Bits[:100])
            self.ui.key_binary.setText(self.generated_password[:100])
            self.ui.encrypted_message.setText(self.encrypted_message[:100])
            self.save()

    def save(self):
        file = open('cellular_automata_info.txt', 'w')
        file.write("Entropy value: ")
        file.write("%s " % self.entropy)
        file.write("\n\nCells number: " + str(self.ui.cells_number.text()) + '\n')
        file.write("\nh parameter: " + str(self.ui.h_box.currentText()) + '\n')
        file.write("\nEntropy acceptance threshold: " + str(self.ui.eat_box.currentText()) + '\n')
        file.write("\nRules:\n")
        if type(self.cellular.rules_list) is list:
            for m in self.cellular.rules_list:
                file.write("%s " % m)
            file.write("\n")
        file.write("\nSeed: " + self.ui.seed_amount_box.text() + "\n")
        file.write("\nIterations:\n")
        for n in self.cellular.generations_list:
            for item in n:
                file.write("%s" % item)
            file.write("\n")
        file.write("\n")

        key_file = open('key.txt','w')
        key_file.write(self.generated_password)
        encrypted_message_file = open('encrypted_message.txt','w')
        encrypted_message_file.write(self.encrypted_message)

    @pyqtSlot()
    def decrypt_clicked(self):
        with open('key.txt', 'r') as myfile:
            key = myfile.read().replace('\n', '')

        with open('encrypted_message.txt', 'r') as myfile:
            encrypted_message = myfile.read().replace('\n', '')
        tmp = self.xor(encrypted_message, key)

        text = self.ui.output_name_box.text()
        if text == "":
            text = "file"
        self.bits_to_file(tmp, text)

    def return_column(self, index):
        tmp = ""
        for i in self.cellular.generations_list:
            tmp += i[index]
        return tmp

    def iterate_iterate(self, iterations_counter):
        for i in range(iterations_counter):
            self.cellular.iterate()
            self.ui.currently_iterate_box.setText('Iteration ' + str(i + 1) + ' out of ' + str(iterations_counter))

    def return_pseudorandom_number_sequence(self, index):
        lista_pomocnicza = self.return_column(index)
        return lista_pomocnicza

    def concatenate_list_data(self, lista_do_polaczenia):
        result = ''
        for element in lista_do_polaczenia:
            result += str(element)
        return result


    def losowe_zera_i_jedynki(self, ilosc_losowych_zer_i_jedynek):
        lista = []
        if type(self.rules) is list:
            ilosc_losowych_zer_i_jedynek = len(self.rules)
        else:
            ilosc_losowych_zer_i_jedynek = len(self.String_Bits) + random.randrange(10)
            while ilosc_losowych_zer_i_jedynek < len(self.String_Bits):
                ilosc_losowych_zer_i_jedynek = len(self.String_Bits) + random.randrange(10)

        for licznik in range(ilosc_losowych_zer_i_jedynek):  # to zwraca losowy stan poczatkowy jezeli user nie wpisal
            lista.append(str(random.randrange(2)))
        return lista


    # teraz ph jest dobrze, nie ruszac
    def liczymy_ph(self, ministring, maxistring):  ### 1101 101010100101011101010010110
        i = 0
        powtorzona_czesc = 0
        licznik_czesci = len(maxistring) - (
                    len(ministring) - 1)
        while i < licznik_czesci:
            if ministring == maxistring[i:i + len(
                    ministring)]:
                powtorzona_czesc += 1
            i += 1

        return powtorzona_czesc / licznik_czesci


    # normalnie dzieli string na czesci o dlugosci h, dajac True zwraca jedynie unikalne elementy
    def string_na_czesci(self, sekwencja, h, unikalne=False):
        czesci = []
        iterator = 0
        while iterator < len(sekwencja) - h + 1:
            czesci.append(sekwencja[iterator:iterator + h])  # TU WSZEDZIE H ZOSTAWIAMY BO TO PRZEKAZANY ARGUMENT
            iterator += h

        if unikalne is True:
            czesci = list(set(czesci))

        return czesci

    def entropia(self, sekwencja):
        entropia_value = 0
        lista_czesci_dzielonych_na_h = self.string_na_czesci(sekwencja, int(self.ui.h_box.currentText()),
                                                             True)  # DOROBIONE pole z h
        k = 2  # liczba mozliwych wartosci, ktora przyjmie komorka
        h = int(self.ui.h_box.currentText())
        limit = k ** h

        i = 0
        for czesc in lista_czesci_dzielonych_na_h:
            if i == limit:
                break
            zmienna = self.liczymy_ph(czesc, sekwencja)
            entropia_value += zmienna * lg2(zmienna)
            i += 1
        return entropia_value * (-1)


    @pyqtSlot()
    def load_image_clicked(self):
        home = str(Path.home())
        self.fname, _fliter = QFileDialog.getOpenFileName(self, 'Open File', home)
        self.ui.image_info.setText("File loaded")
        loaded_color = QColor(0, 255, 0)
        self.ui.frame.setStyleSheet("QWidget { background-color: %s }" % loaded_color.name())

    # zwraca string z bitami z pliku i liczbę bajtow z pliku
    def file_to_bits(self, filename):
        bitstring = ""
        i = 0

        with open(filename, "rb") as f:
            byte = f.read(1)
            number = int.from_bytes(byte, "big")
            bits = '{0:08b}'.format(number)
            bitstring += bits
            while byte:
                i += 1
                byte = f.read(1)
                number = int.from_bytes(byte, "big")
                bits = '{0:08b}'.format(number)
                bitstring += bits
            f.close()
        return bitstring, i

    # zamienia bity na bajty, ktore zapisuje w pliku filename
    def bits_to_file(self, bits, filename):
        bitlist = []
        for iterator in range(int(len(bits)/8) - 1):
            bitlist.append(bits[iterator * 8:iterator * 8 + 8])

        with open(filename, "wb") as f:
            bytes_list = []
            for bit in bitlist:
                liczba = int(bit, 2)
                bytes_list.append(liczba.to_bytes(1, 'big'))
            for byte in bytes_list:
                f.write(byte)
            f.close()




# linijka zwracajaca wartosc z  h - int(self.ui.h_box.currentText())
# int(self.ui.cells_number.text())  getter do cells_number
# double(self.ui.eat_box.currentText()) getter do entropy acceptance threshold


#------------------------------ DODANE 18.02.2019 ------------------------------#

#        self.ui.final_entropy_box.setText('tu wypisywanie entropii na sam koniec')
#        self.ui.currently_iterate_box.setText('tutaj licznik iteracji')
#        self.ui.output_name_box.text('TU_NAZWA_PLIKU.JPG')
