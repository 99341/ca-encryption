from math import log2 as lg2

class test():

    def __init__(self):
        self.kurwa_czworki_unique_szmato = 0

    def liczymy_ph(self, ministring,maxistring): ### 1101 101010100101011101010010110
        i =0
        #licznik_czworek = 0
        powtorzona_czworka = 0
        #while i < len(maxistring)-3:
        licznik_czworek = len(maxistring)-3 #to zamiast petli bo kazda liczba oprocz trzech ostatnich ma swoja czworke
        #    i+=1
        j=0
        while i < licznik_czworek:
            if ministring == maxistring[j:j+4]: #ministring bez nawiasow bo zawsze ma 4
                powtorzona_czworka += 1
            i+=4
        return powtorzona_czworka/licznik_czworek

    import scipy.stats as sc
    def string_na_czesci(self, string_do_podzielenia, h):
        czworki = []
        iterator = 0
        while iterator < len(string_do_podzielenia) - h + 1:
            czworki.append(string_do_podzielenia[iterator:iterator + h])
            iterator += 1

        #czworki_unique = []
        #for c in czworki:
        #    if c not in czworki_unique:
        #        czworki_unique.append(c)
        #        self.kurwa_czworki_unique_szmato+=1

        return czworki #czworki_unique

    def entropia(self, generated_password):
        entropia_value = 0
        lista_czworek = self.string_na_czesci(generated_password,4)  # dorobic pole z h
        print(lista_czworek)
        uzyte_czworki = []
        k = 0
        for czworka in lista_czworek:
            if czworka not in uzyte_czworki:
                if k > 16: break
                zmienna = self.liczymy_ph(czworka, generated_password)
                uzyte_czworki.append(czworka)
                if zmienna > 0:
                   entropia_value += zmienna * lg2(zmienna)
                   k+=1

        print(uzyte_czworki)
        return entropia_value*(-1)

# b = 0011010001010110011110001001101010111100110111101111 wtedy entrpia 1.13

b="00000001001000110100010101100111100010011010101111001101111011111111"
c = test()
print(c.entropia(b))


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