from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import string, random, encrypt_ui
from math import log2 as lg2
import ca


class SecretKey(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = encrypt_ui.Ui_Dialog()
        self.cellular = None
        self.rules = None
        self.entropie = None
        self.ui.setupUi(self)
        self.ui.encrypt_key.clicked.connect(self.encrypt_clicked) #podlacza przycisk do funkcji
        self.ui.decrypt_key.clicked.connect(self.decrypt_clicked) #jw
        self.acceptance_threshold = float(self.ui.eat_box.currentText())
        self.cells_number = 0
        self.entropy = 0

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
    def encrypt_clicked(self):  # zmienia na postac binarna jesli klucz nie jest pusty i robi XOR
        if self.ui.cells_number.text() is not "" and self.ui.text_to_encrypt_box.text() is not "":
            entropia = 0
            while entropia < self.acceptance_threshold:
                if self.ui.radio_specified_rules.isChecked():  # tutaj wchodzi jak sa zaznacozne reguly 90, 105, 150, 165
                    self.generate_recommended_rules(int(self.ui.cells_number.text()))

                else:
                    self.generate_random_rules(int(self.ui.cells_number.text()))

                self.cellular = ca.CellularAutomaton(self.losowe_zera_i_jedynki(len(self.rules)),
                                                     non_uniform_rules=self.rules)
                length = len(self.ui.text_to_encrypt_box.text()) * 8 + random.randrange(3) * 4
                if length < 16 * int(self.ui.h_box.currentText()):
                    length = 16 * int(self.ui.h_box.currentText())
                self.iterate_iterate(length)
                rand_index = random.randrange(0, self.cellular.automaton_length)
                self.generated_password = self.return_pseudorandom_number_sequence(rand_index)
                entropia = self.entropia(self.generated_password)
                print(self.generated_password + " " + str(entropia))

                self.entropy = entropia

                binary_text = self.string2bits(self.ui.text_to_encrypt_box.text())  # wrzuca tekst binarny w okienko

                binary_text_string = ""  # laczy liste binarna tekstu w jeden lancuch
                for bits_key in binary_text:
                    binary_text_string += bits_key

                self.ui.text_binary.setText(binary_text_string)
                self.ui.key_binary.setText(self.generated_password)
                self.ui.encrypted_message.setText(self.xor(self.ui.text_binary.text(), self.ui.key_binary.text()))

                self.save()

    def save(self):
        file = open('output.txt', 'w')
        file.write("Text: \n" + self.ui.text_to_encrypt_box.text())
        file.write("\n")
        file.write("Key: \n" + self.ui.key_binary.text())
        file.write("\n")
        file.write("\nEncrypted message: \n" + self.ui.encrypted_message.text())
        file.write("\n")
        file.write("\nIterations:\n")
        for n in self.cellular.generations_list:
            for item in n:
                file.write("%s" % item)
            file.write("\n")
        file.write("\n")
        file.write("\nEntropy value: ")
        file.write("%s " % self.entropy)
        file.write("\n")
        file.write("\nRules:\n")
        if type(self.cellular.rules_list) is list:
            for m in self.cellular.rules_list:
                file.write("%s " % m)
            file.write("\n")

    @pyqtSlot()
    def decrypt_clicked(self):
        if len(self.ui.text_binary_encrypted.text()) > 0 and len(self.ui.key_binary_encrypted.text()) > 0:
            tmp = self.xor(self.ui.text_binary_encrypted.text(), self.ui.key_binary_encrypted.text())
            i = 0
            lista = []
            while (i + 8 <= len(tmp)):
                lista.append(tmp[i:i + 8])
                i += 8
            self.ui.decrypted_message.setText(self.bits2string(lista))

    def return_column(self, index):
        tmp = ""
        for i in self.cellular.generations_list:
            tmp += i[index]
        return tmp

    def iterate_iterate(self, iterations_counter):
        for i in range(iterations_counter):
            self.cellular.iterate()

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
            ilosc_losowych_zer_i_jedynek = len(self.ui.text_to_encrypt_box.text()) + random.randrange(10)
            while ilosc_losowych_zer_i_jedynek < len(self.ui.text_to_encrypt_box.text()):
                ilosc_losowych_zer_i_jedynek = len(self.ui.text_to_encrypt_box.text()) + random.randrange(10)

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

# linijka zwracajaca wartosc z  h - int(self.ui.h_box.currentText())
# int(self.ui.cells_number.text())  getter do cells_number
# double(self.ui.eat_box.currentText()) getter doo entropy acceptance threshold