import graphviz


class Node:
    def __init__(self, label="", branch="master", origin=None, destination=None, style="", pos=None):
        self.label, self.branch, self.origin, self.destination, self.style, self.pos = (
            label,
            branch,
            origin,
            destination,
            style,
            pos,
        )


class Nodes:
    def __init__(self, nodes, shape="circle"):
        self.nodes = nodes
        self.shape = shape

    def get_range(self):
        return range(len(self.nodes))

    def replace_node(self, previous, next):
        range = self.get_range()
        for i in range:
            if previous == self.nodes[i].label:
                continue
            if previous == self.nodes[i].origin and self.nodes[i].label != next:
                self.nodes[i].origin = next
            if previous == self.nodes[i].destination:  # and self.nodes[i].label != next:
                self.nodes[i].destination = next

    def update_with_style(self):
        range = self.get_range()
        for i in range:

            dpos = 0.5 if "<" in self.nodes[i].style else -0.5

            if "<" in self.nodes[i].style or ">" in self.nodes[i].style:
                n = Node(
                    label=self.nodes[i].label + "i",
                    branch=self.nodes[i].branch,
                    pos=self.nodes[i].pos + dpos,
                    origin=self.nodes[i].origin,
                    destination=self.nodes[i].label,
                    style=self.nodes[i].style + ",point",
                )
                self.replace_node(self.nodes[i].label, n.label)
                self.nodes.append(n)

    def get_edge_style(self, origin, destination, cpos):
        args = dict(color="grey", arrowhead="none", style="solid")
        for n in self.nodes:
            if n.label in [origin, destination] and "dashed" in n.style:
                args.update(dict(style="dashed"))

        return args

    def get_node_style(self, node, branch, dstyle):
        if "purple" in node.style:
            color = "#C06C84"  # 6C5B7B F8B195 C06C84
        elif node.label in "123456789" or "red" in node.style:
            color = "#F67280"  # 6C5B7B F8B195 C06C84
        elif node.label in "ABCDE" or "blue" in node.style:
            color = "#355C7D"  # 6C5B7B F8B195 C06C84
        else:
            color = branch.color

        pos = str(node.pos) + "," + str(branch.pos) + "!"
        args = dict(
            fontsize="10",
            style="filled",
            fontcolor="white",
            fontname="Comic Sans MS",
            shape=self.shape,
            fillcolor=color,
            pos=pos,
        )
        if "point" in node.style:
            args = dict(fontcolor="white", shape="point", color="grey", pos=pos)
        if dstyle == "disable":
            args.update(dict(fontcolor="#E3E3E3", color="#E3E3E3", fillcolor="#F9F9F9"))
        if dstyle == "highlight":
            fontsize = "12" if len(node.label) > 10 else "20"
            args.update(dict(fontcolor="yellow", color="yellow", fillcolor="red", fontsize=fontsize))
        return args


class Branch:
    def __init__(self, label="master", color="master", pos=0):
        self.label, self.color, self.pos = label, color, pos
        self.show_title = True

    def title(self, node, digraph):
        if self.show_title:
            pos = self.pos - 0.5 if self.pos < 0 else self.pos + 0.5
            bpos = str(node.pos) + "," + str(pos) + "!"
            digraph.node(
                node.branch, fontsize="20", pos=bpos, fontcolor=self.color, shape="none", fontname="Comic Sans MS"
            )
            self.show_title = False
