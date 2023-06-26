import IPython
import ipywidgets


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


def dance_puppets2(tag):
    import IPython

    return IPython.display.Javascript(
        """
    var arg = "%s";
    if (arg=="execute_below") {
        IPython.notebook.execute_cells_below();
    }
    else if (arg=="execute_all") {
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
           if ((arg=="toggle" && code.substring(0, 100).includes("@toggle_on")) || 
                    (arg=="hide_code" && code.substring(0, 60).includes("@toggle"))
                    ) {
                cur_cell.set_text(code.replace("#@toggle_on", "#@toggle_off"));
                cur_cell.element.find('div.input').hide();
           }
           else if ((arg=="toggle" && code.substring(0, 60).includes("@toggle_off")) || 
                    (arg=="show_code" && code.substring(0, 60).includes("@toggle"))
                    ) {
                cur_cell.set_text(code.replace("#@toggle_off", "#@toggle_on"));
                //cur_cell.element.show();
                cur_cell.element.find('div.input').show();
           }
           if (arg=="execute_on_start" && code.substring(0, 60).includes("@execute_on_start")) {
                cur_cell.execute();
           }       
        }
    }
    """
        % tag
    )


def dance_puppets(tag):
    import IPython

    return IPython.display.Javascript(
        """
    
    // Find my cell index
    var output_area = this;
    var cell_element = output_area.element.parents('.cell');
    var cell_idx = Jupyter.notebook.get_cell_elements().index(cell_element);
        
    var arg = "%s";
    if (arg.substring(0, 100).includes("@execute_below")) {
        IPython.notebook.execute_cells_below();
    }
    else
    {
        var cells = Jupyter.notebook.get_cells();
        for (var i = 0; i < cells.length; i++) {
           var cur_cell = cells[i];
           var code = cur_cell.get_text();

            if (arg.substring(0, 100).includes("execute_on_start") && code.substring(0, 200).includes("execute_on_start")) {
               if (i != cell_idx) {
                    cur_cell.execute();
                    }
           }       

           if (arg.substring(0, 100).includes("toggle_on") && code.substring(0, 200).includes("toggle_on")) {
                cur_cell.set_text(code.replace("toggle_on", ">toggle_off"));
                cur_cell.element.find('div.input').hide();
           }           
           else if (arg.substring(0, 100).includes("toggle_off") && code.substring(0, 200).includes("toggle_off")) {
                cur_cell.set_text(code.replace("toggle_off", "toggle_on"));
                cur_cell.element.find('div.input').show();
           }
        }
    }
    """
        % tag
    )
