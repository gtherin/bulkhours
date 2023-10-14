

def vizualize(layers):
    import graphviz

    text_from_file = """digraph G {rankdir = LR; splines=false; edge[style=invis]; ranksep= 1.4"""
    colors = ["#0097B2", "#52DE97", "#C70039", "#FF5733", "#FBE555", "#581845", "black"]

    for l in range(len(layers)):
        text_from_file += """{\nnode [shape=circle, color="%s", style=filled, fillcolor="%s", fontcolor=white];\n""" % (colors[l], colors[l])
        for i in range(layers[l]):
            if l == 0:
                text_from_file += f"a{i}{l+1} [label=<x<sub>{i}</sub>>];\n"
            elif l == len(layers)-1 and layers[l] == 1:
                text_from_file += f"a{i}{l+1} [label=<y_hat>];\n"
            else:
                text_from_file += f"a{i}{l+1} [label=<w<sub>{i}</sub><sup>[{l+1}]</sup>>]\n"
        text_from_file += "}\n{rank=same; %s ;}" % ("->".join([f"a{i}{l+1}" for i in range(layers[l])]))

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

    src = graphviz.Source(text_from_file)
    src.render()
    return src