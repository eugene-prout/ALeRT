import graphviz
import pyparsing as pp

class Node(object):
    def __init__(self, tokens):
        self._tokens = tokens
    def __repr__(self):
        return f"{self.__class__.__name__}({self._tokens.asList()})"

class Terminal(Node):
    def __init__(self, tokens: pp.ParseResults):
        self.value = tokens[0]

    def __repr__(self):
        return f"Terminal('{self.value}')"
    
class NonTerminal(Node):
    def __init__(self, tokens):
        self.value = tokens[0]

    def __repr__(self):
        return f"NonTerminal('{self.value}')"

class Derivation(Node):
    def __init__(self, tokens: pp.ParseResults):
        self.symbols = tokens.as_list()

    def __repr__(self):
        return f"Derivation({self.symbols})"

class Production(Node):
    def __init__(self, tokens):
        token_list = tokens.as_list()
        self.head, *self.derivations = token_list

        self.first_set_terminals = []
        self.first_set_nonterminals = []

        for d in self.derivations:
            d: Derivation
            first_symbol = d.symbols[0]
            if type(first_symbol) == Terminal:
                self.first_set_terminals.append(first_symbol)
            elif type(first_symbol) == NonTerminal:
                self.first_set_nonterminals.append(first_symbol)
            
    def __repr__(self):
        return f"Production({self.head},{self.derivations})"

class Grammar(Node):
    def __init__(self, tokens):
        self.productions: list[Production] = tokens.as_list()

    def __repr__(self):
        output = '\n\t'.join(p.__repr__() for p in self.productions)
        return f"Grammar([{output}])"

def generate_grammar():
    terminal = (
        pp.QuotedString('"')
        | pp.Keyword("epsilon")
        | pp.Keyword("IDENT")
        | pp.Keyword("FLOAT_LIT")
        | pp.Keyword("BOOL_LIT")
        | pp.Keyword("INT_LIT")
    )
    terminal.add_parse_action(Terminal)

    non_terminal = pp.Word(pp.alphas + "_")
    non_terminal.add_parse_action(NonTerminal)

    derivation = pp.OneOrMore(terminal | non_terminal, stop_on=pp.White("\n"))
    derivation.add_parse_action(Derivation)

    production = non_terminal + pp.Keyword("::=").suppress() + derivation + pp.ZeroOrMore(pp.Keyword("|").suppress() + derivation)
    production.add_parse_action(Production)

    grammar = pp.OneOrMore(production)
    grammar.add_parse_action(Grammar)
    return grammar

def parse_string(string) -> Grammar:
    grammar = generate_grammar()
    output = grammar.parse_string(string, parse_all=True)
    return output[0] #type: ignore

def calculate_graph(prods: list[Production]) -> tuple[set[str], set[tuple[str, str]]]:
    nodes = set()
    edges = set()
    for p in prods: 
        nodes.add(p.head.value)
        if len(p.first_set_terminals) > 0:
            terminal_node = ",".join(t.value for t in p.first_set_terminals)
            nodes.add(terminal_node)

            edges.add(
                (p.head.value, terminal_node)
            )

        for nt in p.first_set_nonterminals:
            if nt.value not in nodes:
                nodes.add(nt.value)
            edges.add((p.head.value, nt.value))

    return nodes, edges

def render_graph(name: str, nodes: set[str], edges: set[tuple[str, str]]):
    dot = graphviz.Digraph(
        name, strict=True
    )

    for item in nodes:
        dot.node(item)

    for s, t in edges:
        dot.edge(s, t)
    dot.render(directory="doctest-output", view=True)

# file = open("fixed_grammar.bnf").read()
# tree = parse_string(file)

# render_graph("First set dependencies", *calculate_graph(tree.productions))