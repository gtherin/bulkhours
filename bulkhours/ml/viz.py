
from .. import core




def vizualize(layers, activation=None, show_activation=True, filename=None):
    import graphviz
    # size = "7.75,10.25"
    text_from_file = """digraph G {rankdir = LR; splines=false; edge[style=invis]; ranksep= 1.4  """

    colors = [core.c.green,core.c.blue, core.c.red, core.c.purple, core.c.yellow, core.c.black]
    colors[len(layers)-1] = core.c.orange

    def get_label(text, lactivation=None, fname=""):
        activations = {None: text, "RELU": "RELU(%s)" % text, "sigmoid": "&#x3C3;(%s)" % text}
        if not show_activation:
            return """[label =<%s> ];\n""" % (fname)
        if fname != "": fname = fname + "="
        return """[label =<%s%s> ];\n""" % (fname, activations[lactivation])
        #return """[label =<<table border="0" cellborder="0"><tr><td>%s</td></tr><tr><td>%s</td></tr></table>> ];\n""" % (fname, activations[lactivation])

    for l in range(len(layers)):
        text_from_file += """{\nnode [shape=circle, color="%s", style=filled, fillcolor="%s", fontcolor=white];\n""" % (colors[l], colors[l])

        lactivation = None if activation is None or len(activation) <= l else activation[l]

        for i in range(layers[l]):
            text_from_file += f"a{i}{l+1} "

            if l == 0:
                text_from_file += f"[label=<x<sub>{i}</sub>>];\n"
            elif l == len(layers)-1 and layers[l] == 1:
                text_from_file += get_label(f"z<sub>{i}</sub><sup>[{l}]</sup>", lactivation=lactivation, fname="y&#770;")
            elif l == len(layers)-1:
                text_from_file += get_label(f"z<sub>{i}</sub><sup>[{l}]</sup>", lactivation=lactivation, fname=f"y&#770;<sub>{i}</sub>")
            else:
                text_from_file += get_label(f"z<sub>{i}</sub><sup>[{l}]</sup>", lactivation=lactivation, fname=f"a<sub>{i}</sub><sup>[{l}]</sup>")
        text_from_file += "}\n{rank=same; %s ;}" % ("->".join([f"a{i}{l+1}" for i in range(layers[l])]))

    for l in range(len(layers)):
        plabel = "X" if l == 1 else "A<sup>[%s]</sup>" % (l-1)
        lactivation = None if activation is None or len(activation) <= l else activation[l]
        lparam = "Z<sup>[%s]</sup>" % l
        activations = {None: lparam, "RELU": "RELU(%s)" % lparam, "sigmoid": "&#x3C3;(%s)" % lparam}

        if l == 0:
            label = """Input layer""".format(l, l+1)
        elif l == len(layers)-1:
            label = """Output layer:<br/><br/>Z<sup>[{0}]</sup>=W<sup>[{0}]</sup>{2}+b<sup>[{0}]</sup><br/><br/>Y&#770;={3}""".format(l, l+1, plabel, activations[lactivation])
        else:
            label = """Hidden layer {0}:<br/><br/>Z<sup>[{0}]</sup>=W<sup>[{0}]</sup>{2}+b<sup>[{0}]</sup><br/><br/>A<sup>[{0}]</sup>={3}""".format(l, l+1, plabel, activations[lactivation])

        text_from_file += """l{0} [shape=plaintext, label=<{2}>]; l{0}->a0{1}; {{rank=same; l{0};a0{1}}};""".format(l, l+1, label)

    if 0:
        if len(layers) > 0:
            text_from_file += """l0 [shape=plaintext, label="layer 1 (input layer)"]; l0->a01; {rank=same; l0;a01};"""
        if len(layers) > 1:
            text_from_file += """l1 [shape=plaintext, label=<layer 2: Z<sup>[1]</sup>=W<sup>[1]</sup>X+b<sup>[0]</sup>>]; l1->a02; {rank=same; l1;a02};"""
        if len(layers) > 2:
            text_from_file += """l2 [shape=plaintext, label=<layer 3: Z<sup>[2]</sup>=W<sup>[2]</sup>A<sup>[1]</sup>+b<sup>[2]</sup>>]; l2->a03; {rank=same; l2;a03};"""
        if len(layers) > 3:
            text_from_file += """l3 [shape=plaintext, label=<layer 4: Z<sup>[3]</sup>=W<sup>[3]</sup>A<sup>[2]</sup>+b<sup>[3]</sup>>]; l3->a04; {rank=same; l3;a04};"""

    text_from_file += """edge[style=solid, tailport=e, headport=w];"""
    for l in range(len(layers)-1):
        text_from_file += "{%s} -> {%s};" % (";".join([f"a{i}{l+1}" for i in range(layers[l])]), ";".join([f"a{i}{l+2}" for i in range(layers[l+1])]))


    text_from_file += "}"

    grv = graphviz.Source(text_from_file)

    if filename is not None:
        filename = filename.split(".")[0]
        grv.render(filename, format="png")
    else:
        grv.render()
        return grv