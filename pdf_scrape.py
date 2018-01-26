import pdfquery

pdf = pdfquery.PDFQuery("pdfs/induction_of_c-jun_expression_in_the_myeloid-leukemia_cell-line_kg-1_by_1-beta-d-arabinofuranosylcytosine.pdf")

pdf.load()
print(pdf.tree)