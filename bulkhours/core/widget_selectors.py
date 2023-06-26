import ipywidgets

from .widget_base import WidgetBase


class WidgetCheckboxes(WidgetBase):
    widget_id = "checkboxes"
    widget_comp = "lw|sc"

    def init_widget(self):
        self.widget_checkboxes = [
            ipywidgets.Checkbox(value=False, description=i, indent=False) for i in self.cinfo.options.split(";")
        ]
        layout = (
            self.cinfo.layout
            if hasattr(self.cinfo, "layout")
            else ipywidgets.Layout(overflow="scroll hidden", width="auto", flex_flow="row", display="flex")
        )
        return ipywidgets.VBox(children=self.widget_checkboxes, layout=layout)

    def get_answer(self):
        cell_checks = self.cinfo.options.split(";")
        return ";".join([cell_checks[k] for k, i in enumerate(self.widget_checkboxes) if i.value])


class WidgetRadios(WidgetCheckboxes):
    widget_id = "radios"
    widget_comp = "lwsc"

    def init_widget(self):
        return ipywidgets.RadioButtons(options=self.cinfo.options.split(";"), layout={"width": "max-content"})

    def get_answer(self):
        return self.widget.value
