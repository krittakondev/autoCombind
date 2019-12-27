from reportlab.graphics.shapes import Rect, Circle
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import CMYKColorSep

filename = 'cmyk_overprint.pdf'

cyan =    CMYKColorSep(1, 0, 0, 0, spotName='cyan')
magenta = CMYKColorSep(0, 1, 0, 0, spotName='magenta')
yellow =  CMYKColorSep(0, 0, 1, 0, spotName='yellow')
black =   CMYKColorSep(0, 0, 0, 1, spotName='black')

c = Canvas(filename, pagesize=(450,550), cropMarks=True)

c.setFillOverprint(True)


# Overlapping CMY circles

x = 75
y = 525
r = 100

c.setFillColor(cyan)
c.circle(x+(r), y-r, r, fill=True, stroke=False)

c.setFillColor(magenta)
c.circle(x+(r*2), y-r, r, fill=True, stroke=False)

c.setFillColor(yellow)
c.circle(x+(r*1.5), y-r-(0.866025404*r), r, fill=True, stroke=False)



# Gradients

x = 25
h = 25
w = 300
blocks = 5
c.setFont('Helvetica', 7)


# Red, Green, Blue

y = 185
c.setFillColor(cyan)
c.rect(x, y, w, h*0.75, fill=True, stroke=False)
for i in range(0,blocks):
    density = (1.0/(blocks-1))*i
    c.setFillColor(CMYKColorSep(0, 1, 1, 0, spotName='red', density=density))
    c.rect(x+(i*(w/blocks)), y, (w/blocks), h, fill=True, stroke=False)
c.drawString(335, y+10, 'Red overprinted on Cyan')

y = 155
c.setFillColor(cyan)
c.rect(x, y, w, h*0.75, fill=True, stroke=False)
for i in range(0,blocks):
    density = (1.0/(blocks-1))*i
    c.setFillColor(CMYKColorSep(1, 0, 1, 0, spotName='green', density=density))
    c.rect(x+(i*(w/blocks)), y, (w/blocks), h, fill=True, stroke=False)
c.drawString(335, y+10, 'Green overprinted on Cyan')

y = 125
c.setFillColor(cyan)
c.rect(x, y, w, h*0.75, fill=True, stroke=False)
for i in range(0,blocks):
    density = (1.0/(blocks-1))*i
    c.setFillColor(CMYKColorSep(1, 1, 0, 0, spotName='blue', density=density))
    c.rect(x+(i*(w/blocks)), y, (w/blocks), h, fill=True, stroke=False)
c.drawString(335, y+10, 'Blue overprinted on Cyan')


# Pantone

y = 85
c.setFillColor(CMYKColorSep(1, 0.67, 0, 0.23, spotName='PMS_288'))
c.rect(x, y, w, h*0.75, fill=True, stroke=False)
for i in range(0,blocks):
    density = (1.0/(blocks-1))*i
    c.setFillColor(CMYKColorSep(0, 0.55, 1, 0.02, spotName='PMS_717', density=density))
    c.rect(x+(i*(w/blocks)), y, (w/blocks), h, fill=True, stroke=False)
c.drawString(335, y+10, 'Pantone 717 overprinted on 288')

y = 55
c.setFillColor(CMYKColorSep(0, 1, 0.1, 0.35, spotName='PMS_7435'))
c.rect(x, y, w, h*0.75, fill=True, stroke=False)
for i in range(0,blocks):
    density = (1.0/(blocks-1))*i
    c.setFillColor(CMYKColorSep(0.5, 0.7, 0, 0, spotName='PMS_7442', density=density))
    c.rect(x+(i*(w/blocks)), y, (w/blocks), h, fill=True, stroke=False)
c.drawString(335, y+10, 'Pantone 7442 overprinted on 7449')

y = 25
c.setFillColor(CMYKColorSep(0, 0.1, 1, 0, spotName='PMS_109'))
c.rect(x, y, w, h*0.75, fill=True, stroke=False)
for i in range(0,blocks):
    density = (1.0/(blocks-1))*i
    c.setFillColor(CMYKColorSep(0.4, 0, 1, 0.38, spotName='PMS_7496', density=density))
    c.rect(x+(i*(w/blocks)), y, (w/blocks), h, fill=True, stroke=False)
c.drawString(335, y+10, 'Pantone 7496 overprinted on 109')


c.save()
