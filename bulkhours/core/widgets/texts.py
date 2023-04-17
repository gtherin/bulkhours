import ipywidgets

from .buttons import *
from .base import WidgetBase
from .sliders import WidgetIntSlider


class WidgetCodeText(WidgetBase):
    widget_id = "codetext"

    def init_widget(self):
        return ipywidgets.Text(value=self.cinfo.default)

    def get_answer(self):
        print(self.widget)
        print(self.widget.value)
        return eval(self.widget.value)

    def get_params(self):
        print(self.widget)
        print(self.widget.value)
        return dict(
            answer=self.get_answer(), atype=self.cinfo.type, code=self.widget.value, comment=f"'{self.widget.value}'"
        )

    def display_correction(self, data, output=None):
        cc = "" if data["answer"] == data["code"] else f" ({data['code']})"

        if data["answer"] == self.get_answer():
            md(mdbody=f"🥳Correction: {data['answer']}{cc}", bc="green")
        else:
            md(mdbody=f"😔Correction: {data['answer']}{cc}", bc="red")


class WidgetTextArea(WidgetIntSlider):
    widget_id = "textarea"

    def init_widget(self):
        default = "Je ne sais pas" if self.in_french else "I don't know"
        return ipywidgets.Textarea(placeholder=default, disabled=False)

    def get_answer(self):
        return self.cell

    def get_params(self):
        return dict(answer=self.get_answer(), atype=self.cinfo.type, comment=str(self.widget.value))
