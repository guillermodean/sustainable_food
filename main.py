import PyPDF2
import re
import pandas as pd
import os


def main():
    dirs = os.listdir()
    lista = []
    df = pd.DataFrame()
    for file in dirs:
        if "Compra" in file:  # Todos los archivos descargados contienen el nombre compra
            lista.append(file)
            pdfFile = file
            pdfRead = PyPDF2.PdfFileReader(pdfFile)
            page = pdfRead.getPage(0)
            pageContent = page.extractText()  # leo el pdf
            products = re.findall(r'(((\D+)\s+\w+\s+\w+)(\d+\.?\d*))', pageContent)  # busco los campos que me interesan
            df = df.append(products, ignore_index=True)
            df.drop(df.tail(2).index, inplace=True)  # drop last n rows
            # [+-]?([0-9]*[.])?[0-9]+
    df = df.drop(columns=[0, 2])
    print('numero de comras: ' + str(len(lista)))
    df.to_csv('comidas.csv')
    return df


def wrangling_data(df):
    df = df.rename(columns={1: "producto", 3: "precio"})
    df = df[~df.producto.str.contains("CLUBAHORRO|CONSEGUIDOSTOTAL|DESCUENTOS|CONSEGUIDOS",regex=True)]
    df.astype({'precio': 'float32'}).dtypes
    dfgb = df.groupby(by='producto').count()
    productosdistintos=len(df.drop_duplicates())
    print ('hemos consumido en total: '+str(productosdistintos)+' productos distintos')
    print("Productos más consumidos: ")
    print(dfgb.sort_values('precio',ascending=False).head())
    print("Productos más caros: ")
    print(df.sort_values('precio',ascending=False).head())
    df.to_csv('comidas_clean.csv')


if __name__ == "__main__":
    df = main()
    wrangling_data(df)

# TODO sacar los pdfs del source y meterlos en carpeta data
# TODO extraer los procudtos animales y pescados (REGEX)
# Todo graficar los porcentajes
# Todo automatizar la descarga de los pdfS? y updatear todo?
