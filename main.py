import PyPDF2
import re
import pandas as pd
import os

def main ():
    dirs = os.listdir()
    lista = []
    df=pd.DataFrame()
    for file in dirs:
        if "Compra" in file:  #Todos los archivos descargados contienen el nombre compra
            lista.append(file)
            pdfFile = file
            pdfRead = PyPDF2.PdfFileReader(pdfFile)
            page=pdfRead.getPage(0)
            pageContent = page.extractText()  #leo el pdf
            products = re.findall(r'(((\D+)\s+\w+\s+\w+)(\d+\.?\d*))',pageContent) #busco los campos que me interesan
            print(products)
            df=df.append(products,ignore_index=True)
            df.drop(df.tail(2).index, inplace=True)  # drop last n rows
            #[+-]?([0-9]*[.])?[0-9]+
    df=df.drop(columns=[0,2])
    print(df.head())
    print('numero de comras: '+str(len(lista)))
if __name__=="__main__":
    main()

 #TODO extraer los procudtos animales y pescados (REGEX)
 #Todo graficar los porcentajes
 #Todo automatizar la descarga de los pdfS? y updatear todo?