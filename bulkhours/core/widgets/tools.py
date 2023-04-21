import IPython


def md(mdbody=None, header=None, rawbody=None, codebody=None, hc="red", bc="black", icon="📚"):
    print("")
    if header:
        IPython.display.display(
            IPython.display.Markdown(
                f"<b><font face='FiraCode Nerd Font' size=4 color='{hc}'>{header} {icon}:<font></b>"
            )
        )

    if mdbody and (type(mdbody) in [int, float] or len(mdbody) > 1):
        IPython.display.display(
            IPython.display.Markdown(f"<font face='FiraCode Nerd Font' size=4 color='{bc}'>{mdbody}<font>")
        )
    if rawbody and len(rawbody) > 1:
        print(rawbody)
    if codebody and len(codebody) > 1:
        if "g++" in codebody:
            language = "cpp"
        if "nvcc" in codebody:
            language = "cuda"
        else:
            language = None
        IPython.display.display(IPython.display.Code(codebody, language=language))
