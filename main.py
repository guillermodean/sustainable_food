import PyPDF2
import re
import pandas as pd

def main ():
    pdfFile="Compra.pdf"
    pdfRead=PyPDF2.PdfFileReader(pdfFile)
    page=pdfRead.getPage(0)
    pageContent=page.extractText()  #leo el pdf
    print(pageContent)
    products=re.findall(r'(((\D+)\s+\w+\s+\w+)(\d+\.?\d*))',pageContent) #busco los campos que me interesan
    print(products)
    df=pd.DataFrame(products)
    print(df)
    #[+-]?([0-9]*[.])?[0-9]+
if __name__=="__main__":
    main()
 #TODO bucle para todos los archivos de la carpeta del proyecto
 #todo append todos los resultados en un datafram
 #TODO extraer los procudtos animales y pescados (REGEX)
 #Todo graficar los porcentajes
 #Todo automatizar la descarga de los pdfS? y updatear todo?