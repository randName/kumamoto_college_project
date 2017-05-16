from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
from PyPDF2 import PdfFileReader, PdfFileWriter

font_path = "application/static/TakaoExGothic.ttf"
pdfmetrics.registerFont(ttfonts.TTFont("Takao", font_path))

class PdfDocument(object):

    CENTER = 'center'
    RIGHT = 'right'
    LEFT = 'left'
    ALIGN = { CENTER: 'Centred', RIGHT: 'Right' }

    def __init__(self, instream, outstream, font=("Takao", 9)):
        self.base = PdfFileReader(instream)

        self.s = BytesIO()
        self.c = Canvas(self.s, pagesize=A4)

        self.font = font
        self.c.setFont(*self.font)

        self.output = outstream

    def string(self, pos, t, align=LEFT):
        getattr(self.c, 'draw%sString' % self.ALIGN.get(align, ''))(*pos, t)

    def circle(self, pos):
        self.c.circle(*pos, r=10, stroke=1, fill=0)

    def text(self, pos, txt, **kwargs):
        t = self.c.beginText()
        t.setTextOrigin(*pos)
        t.textLines(txt)
        self.c.drawText(t)

    def nextpage(self):
        self.c.showPage()
        self.c.setFont(*self.font)

    def write(self):
        self.c.save()
        self.s.seek(0)

        inp = PdfFileReader(self.s)
        out = PdfFileWriter()

        for i in range(min(inp.getNumPages(), self.base.getNumPages())):
            p = self.base.getPage(i)
            p.mergePage(inp.getPage(i))
            out.addPage(p)

        out.write(self.output)


class PdfForm(object):

    CENTER = 'center'
    RIGHT = 'right'
    LEFT = 'left'

    def __init__(self, d):
        self.d = d

    def shortans(self, position, align=PdfDocument.LEFT):
        def gen(text):
            self.d.string(position, str(text), align)
        return gen

    def longans(self, position):
        def gen(text):
            self.d.text(position, str(text))
        return gen

    def checkbox(self, choices):
        def gen(choice):
            self.d.string(choices.get(choice, (0, 0)), '✓')
        return gen

    def circle(self, choices):
        def gen(choice):
            self.d.circle(choices.get(choice, (0, 0)))
        return gen

    def date(self, posses):
        def gen(d):
            for k, v in posses.items():
                self.d.string(v, d.strftime(k))
        return gen

    def fill(self, values):
        for page in self.fields:
            for k, v in page.items():
                v(values.get(k, ''))
            self.d.nextpage()
        self.d.write()
