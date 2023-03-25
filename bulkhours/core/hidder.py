import IPython
import ipywidgets


def hide_cell(label="Edit question"):
    return IPython.display.HTML(
        """<script>
code_show = true; 
function code_toggle() {
 if (code_show){
     $('div.input').hide();
 } else {
     $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()">
<button id="hns" class="p-Widget jupyter-widgets jupyter-button widget-button mod-link">%s</button>
</form>"""
        % label
    )


def upload_overleaf():
    upload = ipywidgets.FileUpload(
        accept=".zip", multiple=False, description="Upload Overleaf", button_style="success"
    )

    def show_it(inputs):
        import os

        with open("main.zip", "wb") as f:
            # f.write(upload.data[0])
            f.write(upload.value[0]["content"])
        print("Unzip")
        os.system("unzip -o main.zip")
        print("To md")
        os.system("pandoc -s main.tex -o main.md > /dev/null 2>&1")
        print("To pdf")
        #!pdflatex /pathtomyfile.tex
        os.system("pdflatex main.tex > /dev/null 2>&1")
        print("Show")
        with open("main.md", "r") as f:
            md = "\n".join(f.readlines())
            IPython.display.display(IPython.display.Markdown(md))

    def download(inputs):
        from google.colab import files

        files.download("main.pdf")

    upload.observe(show_it, names="value")

    generate = ipywidgets.Button(description="Pdf file", button_style="danger")
    generate.on_click(download)

    return ipywidgets.HBox([upload, generate])
