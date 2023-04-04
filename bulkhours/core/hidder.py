import IPython
import ipywidgets


def dance_puppets(tag):
    return IPython.display.Javascript(
        """
    if ("%s"=="execute_all") {
        IPython.notebook.execute_cells_below();
    }
    else
    {
        var kernel = IPython.notebook.kernel;
        var cells = Jupyter.notebook.get_cells();
        for (var i = 0; i < cells.length; i++) {
           var cur_cell = cells[i];
           var code = cur_cell.get_text();
           var tags = cur_cell._metadata.tags;
           if (tags != undefined) {
               for (var j = 0; j < tags.length; j++) {
                  if (tags[j]=="hide_tag") {
                      cur_cell.element.show();
                  }
                }
           }
           if ("%s"=="toggle") {
               if (code.substring(0, 30).includes("@toggle_on")) {
                    cur_cell.set_text(code.replace("#@toggle_on", "#@toggle_off"));
                    cur_cell.element.find('div.input').hide();
               }
               else if (code.substring(0, 30).includes("@toggle_off")) {
                    cur_cell.set_text(code.replace("#@toggle_off", "#@toggle_on"));
                    //cur_cell.element.show();
                    cur_cell.element.find('div.input').show();
               }
           }
           if ("%s"=="execute_on_start" && code.substring(0, 100).includes("@execute_on_start")) {
                cur_cell.execute();
           }       
        }
    }
    """
        % (tag, tag, tag)
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
