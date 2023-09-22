import ipywidgets

from .widget_base import WidgetBase
from .widget_sliders import WidgetIntSlider
from .tools import md


class WidgetCodeText(WidgetBase):
    widget_id = "codetext"
    widget_comp = "lwsc"

    def init_widget(self):
        if hasattr(self.cinfo, "answer") and self.cinfo.answer != "":
            kwargs = dict(value=self.cinfo.answer)
        elif hasattr(self.cinfo, "default") and self.cinfo.default != "":
            kwargs = dict(value=self.cinfo.default)
        else:
            kwargs = {}

        return ipywidgets.Text(**kwargs)

    def get_answer(self):
        return eval(self.widget.value)

    def display_correction(self, student_data, teacher_data, output=None):
        cc = "" if teacher_data["answer"] == teacher_data["code"] else f" ({teacher_data['code']})"

        if teacher_data["answer"] == self.get_answer():
            md(mdbody=f"🥳Correction: {teacher_data['answer']}{cc}", bc="green")
        else:
            md(mdbody=f"😔Correction: {teacher_data['answer']}{cc}", bc="red")


class WidgetTextArea(WidgetIntSlider):
    widget_id = "textarea"
    widget_comp = "lwsc"

    def init_widget(self):
        if hasattr(self.cinfo, "answer") and self.cinfo.answer != "":
            kwargs = dict(placeholder=self.cinfo.answer)
        elif hasattr(self.cinfo, "default") and self.cinfo.default != "":
            kwargs = dict(placeholder=self.cinfo.default)
        else:
            kwargs = dict(placeholder="Je ne sais pas" if self.cinfo.language == "fr" else "I don't know")

        return ipywidgets.Textarea(**kwargs)

    def get_answer(self):
        return self.cell
