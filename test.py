import pdfrw

p = {}
#p["/MediaBox"] = {['0.0', '0.0', '595.32', '841.92']}
#p["/Type"] = "/Page"
print(p)
write = pdfrw.PdfWriter()
#print(PdfName.Page)
write.addpage(p)
#write.write("testb.pdf")