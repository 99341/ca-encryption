class CellularAutomaton:
    # generation - poczatkowe ustawienie komorek w automacie
    # uniform_rule - jednakowa zasada dla wszystkich komorek (podajemy jaka)
    # non_uniform_rules - podajemy liste zasad dla poszczegolnych komorek
    def __init__(self, generation, uniform_rule=None, non_uniform_rules=None):
        self.generations_list = []
        self.current_generation = generation
        self.automaton_length = len(generation)
        if uniform_rule is not None:
            self.rules_list = []
            for i in range(self.automaton_length):
                self.rules_list.append(uniform_rule)
        elif non_uniform_rules is not None:
            self.rules_list = non_uniform_rules

    # generowanie stanu komorki o indeksie index w nowej generacji
    # tego nie uzywamy poza klasa
    def create_new_number(self, index):
        rule = bin(self.rules_list[index])
        rule = str(rule[2:]).zfill(8)
        rule = list(rule)
        rule.reverse()
        if self.current_generation[index - 1] == '0' and self.current_generation[index] == '0' and self.current_generation[(index + 1)%self.automaton_length] == '0':
            return rule[0]
        if self.current_generation[index - 1] == '0' and self.current_generation[index] == '0' and self.current_generation[(index + 1)%self.automaton_length] == '1':
            return rule[1]
        if self.current_generation[index - 1] == '0' and self.current_generation[index] == '1' and self.current_generation[(index + 1)%self.automaton_length] == '0':
            return rule[2]
        if self.current_generation[index - 1] == '0' and self.current_generation[index] == '1' and self.current_generation[(index + 1)%self.automaton_length] == '1':
            return rule[3]
        if self.current_generation[index - 1] == '1' and self.current_generation[index] == '0' and self.current_generation[(index + 1)%self.automaton_length] == '0':
            return rule[4]
        if self.current_generation[index - 1] == '1' and self.current_generation[index] == '0' and self.current_generation[(index + 1)%self.automaton_length] == '1':
            return rule[5]
        if self.current_generation[index - 1] == '1' and self.current_generation[index] == '1' and self.current_generation[(index + 1)%self.automaton_length] == '0':
            return rule[6]
        if self.current_generation[index - 1] == '1' and self.current_generation[index] == '1' and self.current_generation[(index + 1)%self.automaton_length] == '1':
            return rule[7]

    # iteruje automat komorkowy
    # stara generacja jest zapisywana na liscie
    # nowa przypisywana jest do pola current_generation
    def iterate(self):
        new_gen = []
        for i in range(self.automaton_length):
            new_gen.append(self.create_new_number(i))
        self.generations_list.append(self.current_generation)
        self.current_generation = new_gen

#cellular = CellularAutomaton(['0', '0', '0', '0', '1', '0', '0', '0'], 53)#, non_uniform_rules=[53, 110, 34, 21, 3,43,9,2,3])
#print("Rules: " + str(cellular.rules_list))


