from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import string, random, encrypt_ui
import ca

class Secret_key(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = encrypt_ui.Ui_Dialog()
        self.cellular = None
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

    @pyqtSlot()
    def encrypt_clicked(self): #zmienai na postac binarna jesli klucz nie jest pusty i robi XOR
        if self.ui.rule_box.text() is not "": #wykona sie tylko jezeli podamy regule
            if self.ui.initial_state.text() is "": #tutaj wchodzi bez podanych wartosci poczatkowych
                self.cellular = ca.CellularAutomaton(self.losowe_zera_i_jedynki(len(self.ui.text_binary_encrypted.text())+random.randrange(10)), int(self.ui.rule_box.text()))
            else:  #tutaj wchodzi z podanymi wartosciami poczatkowymi
                self.cellular = ca.CellularAutomaton(
                    self.nielosowe_zera_i_jedynki() , int(self.ui.rule_box.text()))

            self.iterate_iterate() # tworzy generacje

            print(self.return_haslo_8bit()) #bierze 1 bit z kazdej generacji i tworzy 8 bitowy klucz w postaci listy

            print(self.concatenate_list_data(self.return_haslo_8bit())) #laczy powyzsza liste w stringa
            binary_text = self.string2bits(self.ui.text_to_encrypt_box.text()) # wrzuca tekst binarny w okienko

            binary_text_string = "" #laczy liste binarna tekstu w jeden lancuch
            for bits_key in binary_text:
                binary_text_string += bits_key

            self.ui.generated_key_box.setText(self.bits2string(self.return_haslo_8bit()))
            self.ui.text_binary.setText(binary_text_string)
            self.ui.key_binary.setText(self.concatenate_list_data(self.return_haslo_8bit()))
            self.ui.encrypted_message.setText(self.xor(self.ui.text_binary.text(),self.ui.key_binary.text()))

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

    def return_kolumna(self,index):
        tmp = ""
        for i in self.cellular.generations_list:
            tmp += i[index]
        return tmp

    def iterate_iterate(self):
        for i in range(8):
            self.cellular.iterate()

    def return_haslo_8bit(self):

        lista_pomocnicza = []
        for j in range(self.cellular.automaton_length):
            lista_pomocnicza.append(self.return_kolumna(j))

        return lista_pomocnicza

    def concatenate_list_data(self, list):
        result = ''
        for element in list:
            result += str(element)
        return result

    def nielosowe_zera_i_jedynki(self):
        lista = []
        tmp = self.ui.initial_state.text()
        for licznik in range(len(self.ui.initial_state.text())):  # to zwraca losowy stan poczatkowy jezeli user nie wpisal
            lista.append(str(tmp[licznik]))
        return lista

    def losowe_zera_i_jedynki(self,ilosc_losowych_zer_i_jedynek):
        lista = []
        while ilosc_losowych_zer_i_jedynek < len(self.ui.text_to_encrypt_box.text()):
            #bez tego czasem klucz generowal sie krotszy niz tekst do zaszyfrowania,ale tym to naprawilem
            #hasztag programowanie ekstremalne
            ilosc_losowych_zer_i_jedynek = len(self.ui.text_to_encrypt_box.text()) +random.randrange(len(self.ui.text_to_encrypt_box.text()))

        for licznik in range(ilosc_losowych_zer_i_jedynek): #to zwraca losowy stan poczatkowy jezeli user nie wpisal
            lista.append(str(random.randrange(2)))
        return lista
