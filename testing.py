from math import log2 as lg2

class test():

    def __init__(self):
        self.kurwa_czworki_unique_szmato = 0

    # teraz ph jest dobrze, nie ruszac
    def liczymy_ph(self, ministring,maxistring): ### 1101 101010100101011101010010110
        i = 0
        powtorzona_czworka = 0
        licznik_czworek = len(maxistring)-3 #to zamiast petli bo kazda liczba oprocz trzech ostatnich ma swoja czworke
        while i < licznik_czworek:
            if ministring == maxistring[i:i+4]: #ministring bez nawiasow bo zawsze ma 4
                powtorzona_czworka += 1
            i += 1

        return powtorzona_czworka/licznik_czworek

    # normalnie dzieli string na czesci o dlugosci h, dajac True zwraca jedynie unikalne elementy
    def string_na_czesci(self, string_do_podzielenia, h, unikalne=False):
        czworki = []
        iterator = 0
        while iterator < len(string_do_podzielenia) - h + 1:
            czworki.append(string_do_podzielenia[iterator:iterator + h])
            iterator += h

        if unikalne is True:
            czworki = list(set(czworki))

        return czworki

    '''
    def entropia(self, generated_password):
        entropy_value = 0
        lista_czworek = self.string_na_czesci(generated_password, 4, True)  # dorobic pole z h
        print(lista_czworek)
        uzyte_czworki = []
        k = 0
        for czworka in lista_czworek:
            if czworka not in uzyte_czworki:
                if k > 16:
                    break
                zmienna = self.liczymy_ph(czworka, generated_password)
                uzyte_czworki.append(czworka)
                if zmienna > 0:
                   entropy_value += zmienna * lg2(zmienna)
                   k+=1

        print(uzyte_czworki)
        return entropy_value*(-1)
    '''

    # ta wersja metody styknie, teraz daje ten sam wynik co ta wyzej
    def entropia(self, generated_password):
        entropia_value = 0
        lista_czworek = self.string_na_czesci(generated_password, 4, True) # dorobic pole z h

        for czworka in lista_czworek:
            zmienna = self.liczymy_ph(czworka, generated_password)
            entropia_value += zmienna*lg2(zmienna)

        return entropia_value*(-1)


# b = 0011010001010110011110001001101010111100110111101111 wtedy entrpia 1.13

b="00000001001000110100010101100111100010011010101111001101111011111111"
d = "00010001000010010000100000100000001100000001"
c = test()
print(c.entropia(b))

#1101 101010100101011101010010110
print(c.liczymy_ph("1101", "101010100101011101010010110"))

print(c.string_na_czesci("101010100101011101010010110", 4, True))


# na tym sie wzorowalem
import numpy as np
def entropy2(labels, base=None):
  """ Computes entropy of label distribution. """

  n_labels = len(labels)

  if n_labels <= 1:
    return 0

  value,counts = np.unique(labels, return_counts=True)
  probs = counts / n_labels
  n_classes = np.count_nonzero(probs)

  if n_classes <= 1:
    return 0

  ent = 0.

  # Compute entropy
  #base = e if base is None else base
  for i in probs:
    ent -= i * lg2(i)

  return ent