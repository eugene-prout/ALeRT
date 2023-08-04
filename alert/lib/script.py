from typing import List
import uuid
import pyparsing as pp
import graphviz

terminal = pp.Group(pp.QuotedString('"') | pp.Keyword("epsilon") | pp.Keyword("IDENT") | pp.Keyword("FLOAT_LIT") | pp.Keyword("BOOL_LIT") | pp.Keyword("INT_LIT")).set_results_name("terminal")
non_terminal = pp.Group(pp.Word(pp.alphas+"_")).set_results_name("non-terminal")

expression = pp.OneOrMore(pp.Group(terminal | non_terminal), stop_on=pp.White("\n"))

head = pp.Word(pp.alphas+"_").set_results_name("head")
body = pp.Group(pp.Group(expression) + pp.ZeroOrMore(pp.Keyword("|").suppress() + pp.Group(expression))).set_results_name("body")

production = pp.Group(head + pp.Keyword("::=") + body).set_results_name("production")
grammar = pp.OneOrMore(pp.Group(production)).set_results_name("grammar")

rules = grammar.parse_file("lr.bnf", parse_all=True).as_dict()

class NonTerminal():
    def __init__(self, name, dependencies) -> None:
        self.name = name
        self.dependencies = []
        self.top_level_terminals = None
    def __str__(self):
        return f"{self.name}"

class Terminal():
    def __init__(self, value) -> None:
        self.value = value

class TerminalSet():
    def __init__(self, terminals: List[Terminal]):
        self.value = [x.value for x in terminals]
    def get_rep(self) -> str:
        return ",".join(self.value)

non_terminals = {}

terminals = {"epsilon": Terminal("epislon")}
terminal_sets = {}

for _production in rules["grammar"]:
    _p = _production["production"]
    non_terminals[_p["head"]] = NonTerminal(_p["head"], None)
    derivations = _p["body"]
    for d in derivations:
        for item in d:
            if "terminal" in item:
                value = item["terminal"][0]
                terminals[value] = Terminal(value)

terminal_set_map = {}

for _production in rules["grammar"]:
    _p = _production["production"]
    derivations = _p["body"]
    terminals_set = []
    for d in derivations:
        first_element_of_deriv = d[0]
        if "non-terminal" in first_element_of_deriv:
            non_terminals[_p["head"]].dependencies.append(non_terminals[first_element_of_deriv["non-terminal"][0]])
        if "terminal" in first_element_of_deriv:
            terminals_set.append(terminals[first_element_of_deriv["terminal"][0]])

    if len(terminals_set) > 0:
        new_set = TerminalSet(terminals_set)
        if new_set.get_rep() not in terminal_set_map:
            terminal_set_map[new_set.get_rep()] = new_set
            non_terminals[_p["head"]].top_level_terminals = new_set
        else:
            non_terminals[_p["head"]].top_level_terminals = terminal_set_map[new_set.get_rep()]
    
dot = graphviz.Digraph(str(uuid.uuid4()), comment='First set dependencies', strict=True)  

for item in terminal_set_map.values():
    dot.node(item.get_rep())

for item in non_terminals.values():
    new_node = dot.node(item.name)  

for item in non_terminals.values():
    for dest in item.dependencies:
        dot.edge(item.name, dest.name)
    if item.top_level_terminals is not None:
            dot.edge(item.name, item.top_level_terminals.get_rep())

dot.render(directory='doctest-output', view=True) 