from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import string, random, encrypt_ui
from math import log2 as lg2
import ca

class Secret_key(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = encrypt_ui.Ui_Dialog()
        self.cellular = None
        self.rules = None
        self.entropie = None
        self.ui.setupUi(self)
        self.ui.encrypt_key.clicked.connect(self.encrypt_clicked) #podlacza przycisk do funckji
        self.ui.decrypt_key.clicked.connect(self.decrypt_clicked)

    def id_generator(self, size, chars=string.digits + string.ascii_letters):
        return str(''.join(random.choice(chars) for _ in range(size))) #generuje klucz, tu musza byc automaty

    def string2bits(self, s=''): #bardzo madra funkcja pozyczona ze stackoverflow, zmienia text na bity
        return [bin(ord(x))[2:].zfill(8) for x in s]

    def bits2string(self, b=None): #tym bedziemy odkodowywac, jeszcze nie dziala
        return ''.join([chr(int(x, 2)) for x in b])

    def xor(self, x1, x2): #robi xora, nic tlumaczyc nie trzeba wystarczylo uwazac u franka
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

    def check_if_non_uniform(self):
        tmp = self.ui.rule_box.text()
        for n in range(len(tmp)):
            if tmp[n] == " ":
                return True

        return False

    '''
    @pyqtSlot()
    def encrypt_clicked(self): #zmienai na postac binarna jesli klucz nie jest pusty i robi XOR
        if self.ui.rule_box.text() is not "": #wykona sie tylko jezeli podamy regule

            if self.check_if_non_uniform():
                tmp = self.ui.rule_box.text()
                self.rules = tmp.split(' ')
                self.rules = list(map(int, self.rules))
            else:
                self.rules = [self.ui.rule_box.text()]

            if len(self.rules) == 1:
                self.rules = int(self.rules[0])

                if self.ui.initial_state.text() is "": #tutaj wchodzi bez podanych wartosci poczatkowych
                    self.cellular = ca.CellularAutomaton(self.losowe_zera_i_jedynki(len(self.ui.text_binary_encrypted.text())+random.randrange(10)), self.rules)
                else:  #tutaj wchodzi z podanymi wartosciami poczatkowymi
                    self.cellular = ca.CellularAutomaton(
                        self.nielosowe_zera_i_jedynki(), self.rules)
            else:
                if self.ui.initial_state.text() is "": #tutaj wchodzi bez podanych wartosci poczatkowych
                    self.cellular = ca.CellularAutomaton(self.losowe_zera_i_jedynki(len(self.rules)), non_uniform_rules=self.rules)
                else:  #tutaj wchodzi z podanymi wartosciami poczatkowymi
                    self.cellular = ca.CellularAutomaton(
                        self.nielosowe_zera_i_jedynki(), non_uniform_rules=self.rules)

            self.iterate_iterate(len(self.ui.text_to_encrypt_box.text())*8+random.randrange(3)*4) # tworzy generacje

            self.generated_password = self.return_pseudorandom_number_sequence(0)


            print(self.return_pseudorandom_number_sequence(0)) #bierze 1 bit z kazdej generacji i tworzy 8 bitowy klucz w postaci listy

            print(self.concatenate_list_data(self.return_pseudorandom_number_sequence(0))) #laczy powyzsza liste w stringa
            binary_text = self.string2bits(self.ui.text_to_encrypt_box.text()) # wrzuca tekst binarny w okienko

            binary_text_string = "" #laczy liste binarna tekstu w jeden lancuch
            for bits_key in binary_text:
                binary_text_string += bits_key

            #self.ui.generated_key_box.setText(self.bits2string(self.return_haslo_8bit()))
            self.ui.text_binary.setText(binary_text_string)
            self.ui.key_binary.setText(self.return_pseudorandom_number_sequence(0))
            self.ui.encrypted_message.setText(self.xor(self.ui.text_binary.text(),self.ui.key_binary.text()))

            self.save()
            
    '''

    @pyqtSlot()
    def encrypt_clicked(self):  # zmienai na postac binarna jesli klucz nie jest pusty i robi XOR
        if self.ui.rule_box.text() is not "":  # wykona sie tylko jezeli podamy regule

            if self.check_if_non_uniform():
                tmp = self.ui.rule_box.text()
                self.rules = tmp.split(' ')
                self.rules = list(map(int, self.rules))
            else:
                self.rules = [self.ui.rule_box.text()]

            if len(self.rules) == 1:
                self.rules = int(self.rules[0])

                if self.ui.initial_state.text() is "":  # tutaj wchodzi bez podanych wartosci poczatkowych
                    self.cellular = ca.CellularAutomaton(
                        self.losowe_zera_i_jedynki(len(self.ui.text_binary_encrypted.text()) + random.randrange(10)),
                        self.rules)
                else:  # tutaj wchodzi z podanymi wartosciami poczatkowymi
                    self.cellular = ca.CellularAutomaton(
                        self.nielosowe_zera_i_jedynki(), self.rules)
            else:
                if self.ui.initial_state.text() is "":  # tutaj wchodzi bez podanych wartosci poczatkowych
                    self.cellular = ca.CellularAutomaton(self.losowe_zera_i_jedynki(len(self.rules)),
                                                         non_uniform_rules=self.rules)
                else:  # tutaj wchodzi z podanymi wartosciami poczatkowymi
                    self.cellular = ca.CellularAutomaton(
                        self.nielosowe_zera_i_jedynki(), non_uniform_rules=self.rules)

            self.iterate_iterate(
                len(self.ui.text_to_encrypt_box.text()) * 8 + random.randrange(3) * 4)  # tworzy generacje

            # wylicza entropie dla wszystkich kolumn
            self.entropie = []
            for i in range(self.cellular.automaton_length):
                self.entropie.append(self.entropia(self.return_pseudorandom_number_sequence(i)))
                print(self.entropie[i])

            # wybiera kolumne o najwiekszej entropii
            self.generated_password = self.return_pseudorandom_number_sequence(self.entropie.index(max(self.entropie)))

            print(self.return_pseudorandom_number_sequence(
                0))  # bierze 1 bit z kazdej generacji i tworzy 8 bitowy klucz w postaci listy

            print(self.concatenate_list_data(
                self.return_pseudorandom_number_sequence(0)))  # laczy powyzsza liste w stringa
            binary_text = self.string2bits(self.ui.text_to_encrypt_box.text())  # wrzuca tekst binarny w okienko

            binary_text_string = ""  # laczy liste binarna tekstu w jeden lancuch
            for bits_key in binary_text:
                binary_text_string += bits_key

            # self.ui.generated_key_box.setText(self.bits2string(self.return_haslo_8bit()))
            self.ui.text_binary.setText(binary_text_string)
            self.ui.key_binary.setText(self.generated_password)
            self.ui.encrypted_message.setText(self.xor(self.ui.text_binary.text(), self.ui.key_binary.text()))

            self.save()

    def save(self):
        file = open('output.txt','w')
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
        file.write("\nEntropy values:\n")
        for val in self.entropie:
            file.write("%s " % val)
        file.write("\n")
        file.write("\nRules:\n")
        if type(self.cellular.rules_list) is list:
            # print(self.cellular.rules_list)
            for m in self.cellular.rules_list:
                file.write("%s " % m)
            file.write("\n")

    @pyqtSlot()
    def decrypt_clicked(self):
        if len(self.ui.text_binary_encrypted.text())>0 and len(self.ui.key_binary_encrypted.text())>0:
            tmp = self.xor(self.ui.text_binary_encrypted.text(),self.ui.key_binary_encrypted.text())
            i=0
            lista = []
            while(i+8<=len(tmp)):
                lista.append(tmp[i:i+8])
                i+=8
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



         # lista_pomocnicza = []
         # for j in range(self.cellular.automaton_length):
         #   lista_pomocnicza.append(self.return_kolumna(j))

        return lista_pomocnicza

    def concatenate_list_data(self, lista_do_polaczenia):
        result = ''
        for element in lista_do_polaczenia:
            result += str(element)
        return result

    def nielosowe_zera_i_jedynki(self):
        lista = []
        tmp = self.ui.initial_state.text()
        for licznik in range(len(self.ui.initial_state.text())):  # to zwraca losowy stan poczatkowy jezeli user nie wpisal
            lista.append(str(tmp[licznik]))
        return lista

    def losowe_zera_i_jedynki(self, ilosc_losowych_zer_i_jedynek):
        lista = []
        if type(self.rules) is list:
            ilosc_losowych_zer_i_jedynek = len(self.rules)
        else:
            ilosc_losowych_zer_i_jedynek = len(self.ui.text_to_encrypt_box.text()) + random.randrange(10)
            while ilosc_losowych_zer_i_jedynek  < len(self.ui.text_to_encrypt_box.text()):
                ilosc_losowych_zer_i_jedynek = len(self.ui.text_to_encrypt_box.text()) + random.randrange(10)

        for licznik in range(ilosc_losowych_zer_i_jedynek): #to zwraca losowy stan poczatkowy jezeli user nie wpisal
            lista.append(str(random.randrange(2)))
        return lista

    '''
    def liczymy_ph(self, ministring,maxistring): ### 1101 101010100101011101010010110
        i =0
        licznik_czworek = 0
        powtorzona_czworka = 0
        while i <len(maxistring)-3:
            licznik_czworek += 1

        while i < licznik_czworek:
            if ministring[0:3] == maxistring[i:i+3]:
                powtorzona_czworka += 1

        return powtorzona_czworka/licznik_czworek
    '''

    # teraz ph jest dobrze, nie ruszac
    def liczymy_ph(self, ministring,maxistring): ### 1101 101010100101011101010010110
        i = 0
        powtorzona_czesc = 0
        licznik_czesci = len(maxistring)-(len(ministring)-1) #to zamiast petli bo kazda liczba oprocz trzech ostatnich ma swoja czworke
                                            #to wyzej moze przerobic na: int"(self.ui.comboBox.currentText())-1"
                                            # zamiast -3 na sztywno, bo z 2 sie wykrzaczy
        while i < licznik_czesci:
            if ministring == maxistring[i:i+len(ministring)]: #ministring bez nawiasow bo zawsze ma 4, TO CHYBA TEZ TRZEBA ZMIENIC
                powtorzona_czesc += 1
            i += 1

        return powtorzona_czesc/licznik_czesci
    '''
    def string_na_czesci(self,h):
        czworki = []
        iterator = 0
        while iterator < len(self.generated_password) - h+1:
            czworki.append(self.generated_password[iterator:iterator+h])
            iterator+=h
        return czworki
    '''

    # normalnie dzieli string na czesci o dlugosci h, dajac True zwraca jedynie unikalne elementy
    def string_na_czesci(self, sekwencja,  h, unikalne=False):
        czesci = []
        iterator = 0
        while iterator < len(sekwencja) - h + 1:
            czesci.append(sekwencja[iterator:iterator + h]) #TU WSZEDZIE H ZOSTAWIAMY BO TO PRZEKAZANY ARGUMENT
            iterator += h

        if unikalne is True:
            czesci = list(set(czesci))

        return czesci

    def entropia(self, sekwencja):
        entropia_value = 0
        lista_czesci_dzielonych_na_h = self.string_na_czesci(sekwencja, int(self.ui.comboBox.currentText()), True) # DOROBIONE pole z h
        k = 2  # liczba mozliwych wartosci, ktora przyjmie komorka
        h = int(self.ui.comboBox.currentText())
        limit = k ** h

        i = 0
        for czesc in lista_czesci_dzielonych_na_h:
            if i == limit:
                break
            zmienna = self.liczymy_ph(czesc, sekwencja)
            entropia_value += zmienna*lg2(zmienna)
            i += 1

        return entropia_value*(-1)

#linijka zwracajaca wartosc z  h - int(self.ui.comboBox.currentText())
