import os
import datetime

from .. import data
from .. import core

def format_num(price):
    return "{:.2f}".format(price, ",").replace(",", " ").replace(".", ",")

def format_price(price):
    return format_num(price) + " €"


def format_date(date):
    mois = [
        "Janvier",
        "Fevrier",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Aout",
        "Septembre",
        "Octobre",
        "Novembre",
        "Decembre",
    ]

    return date.strftime("%-d ") + mois[date.month - 1] + date.strftime(" %Y")


class Invoice:

    @staticmethod
    def set_db_info(user, einfo):
        Invoice.accounting = data.get_data(einfo[user]["accounting"], credit=False)
        Invoice.entities = data.get_data(einfo[user]["entities"], credit=False)
        Invoice.einfo = einfo[user]

        # Only keep invoice_ids with existing invoices
        Invoice.accounting = Invoice.accounting[Invoice.accounting["invoice_id"].str.len() > 2]

    def __init__(self, name, invoice_id, df, doc_type="FACTURE"):

        self.client, self.provider = df["client"].iloc[0], df["provider"].iloc[0]
        self.name = name
        self.invoice_id = invoice_id
        self.doc_type = doc_type

        self.transactions = []
        self.data = {}
        self.data["provider"] = Invoice.entities.set_index("client").loc[self.provider].to_dict()
        self.data["provider"]["logo"] = Invoice.einfo["logo"]

        self.data["client"] = Invoice.entities.set_index("client").loc[self.client].to_dict()
        for k, v in self.data["provider"].copy().items():
            if v == "" or v != v:
                del self.data["provider"][k]

        for k, v in self.data["client"].copy().items():
            if v == "" or v != v:
                del self.data["client"][k]
        self.add_dates(df)
        self.add_transactions(df)

    def add_dates(self, df):
        import calendar

        self.date = df["invoice_date"].iloc[0]
        self.invoice_date = df["invoice_date"].iloc[0]

        year, month = int(self.invoice_date.split("-")[0]), int(self.invoice_date.split("-")[1])
        self.invoice_date = datetime.datetime(year, month, int(self.invoice_date.split("-")[2]))
        if "start_date" in df.columns:
            start_date = datetime.datetime.strptime(df["start_date"].unique()[0], "%Y-%m-%d")
            end_date = datetime.datetime.strptime(df["end_date"].unique()[0], "%Y-%m-%d")
        else:
            start_date = datetime.datetime(year, month, 1)
            end_date = datetime.datetime(year, month, calendar.monthrange(year, month)[1])

        self.data.update(
            {
                "invoice_month": self.date,
                "start_date": format_date(start_date),
                "end_date": format_date(end_date),
                "date": self.invoice_date.strftime("%Y-%m-%d"),
                "invoice_date": format_date(self.invoice_date),
                "vat": format_num(0) + "%",
            }
        )

    def add_transactions(self, df):

        trs = []
        subtotal = 0.0
        for tr in df.to_dict(orient='records'):
            tr["service"] = tr["prestation"]
            if type(tr["qty"]) == int:
                tr["rhours"] = tr["qty"]
            else:
                tr["rhours"] = float(tr["qty"].replace(" ", "").replace(",", "."))
            tr["rrate"] = float(tr["rate_ht"].replace(" ", "").replace(",", "."))
            tr["total"] = format_price(rtotal := tr["rhours"] * tr["rrate"])
            tr["rate"] = format_price(tr["rrate"])
            tr["hours"] = format_num(tr["rhours"])
            subtotal += rtotal
            trs.append(tr)

        self.data["subinvoices"] = trs
        self.data["subtotal"] = format_price(subtotal)
        self.data["vat_amount"] = format_price(vat_amount := subtotal * 0)
        self.data["total"] = format_price(subtotal - vat_amount)
        self.data['invoice_id'] = self.invoice_id
        self.data['doc_type'] = self.doc_type

    def generate_html(self):

        from jinja2 import Environment, FileSystemLoader

        # Load the HTML template
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template(self.einfo["template"] + ".html")

        # Render the template with the dynamic data
        invoice = template.render(self.data)

        doc_type = "annex" if self.doc_type in ["FACTURE", "Facture"] else "costimation"

        with open(filename := f"{self.data['invoice_id']}_{self.client}_{doc_type}.html", "w") as f:
            f.write(invoice)
        print(f"Generate files and {filename[:-4]}pdf (from) {filename}")
        os.system(f"wkhtmltopdf --enable-local-file-access {filename} {filename[:-4]}pdf")
        os.system(f"rm -rf {filename}")
        return f"{filename[:-4]}pdf"

    @staticmethod
    def generate_invoices(user, info, outdir=None, doc_type="FACTURE") -> None:
        
        Invoice.set_db_info(user, info)

        if outdir is not None:
            os.system(f"mkdir -p {outdir}")
            cdir = os.getcwd()

            os.chdir(outdir)
            print(os.getcwd())
        
        filelists = ["BulkHours.png", "dart.png", Invoice.einfo['template'] + ".html", Invoice.einfo['template'] + ".css"]

        for f in filelists:
            hfile = core.tools.abspath(f"data/{f}")
            os.system(f"cp {hfile} {f}")

        files = []
        for invoice_id, df in Invoice.accounting.groupby("invoice_id"):
            files.append(Invoice(user, invoice_id, df, doc_type=doc_type).generate_html())

        for f in filelists:
            os.system(f"rm -rf {f}")

        if outdir is not None:
            os.chdir(cdir)
            print(os.getcwd())
        return files
