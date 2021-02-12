import PyPDF2
import re
import pandas as pd
import os


def main():
    dirs = os.listdir()
    lista = []
    df = pd.DataFrame()
    n=0
    for file in dirs:
        if "Compra" in file:  # Todos los archivos descargados contienen el nombre compra, TODO añadir nombre compra

            lista.append(file)
            pdfFile = file
            pdfRead = PyPDF2.PdfFileReader(pdfFile)
            page = pdfRead.getPage(0)  #leer más paginas????
            pageContent = page.extractText()  # leo el pdf
            products = (re.findall(r'(((\D+)\s+\w+\s+\w+)(\d+\.?\d*))', pageContent))  # busco los campos que me interesan  otra opcion [+-]?([0-9]*[.])?[0-9]+
            fecha = (re.findall(r'\d{1,2}\s\-\s[0-9]+\s\-\s[0-9]+',pageContent))
            if n==0:
                df = df.append(products, ignore_index=True)
                df['Fecha']=str(fecha)
            else:
                df = df.append(products, ignore_index=True)
                df['Fecha'] = df['Fecha'].fillna(str(fecha))
            n += 1
            print (df)
            df.drop(df.tail(2).index, inplace=True)  # drop last n rows
    df = df.drop(columns=[0, 2])
    print('numero de comras: ' + str(len(lista)))
    df.to_csv('comidas.csv')
    return df
#06 - 11 - 2020  d{1,2}-\\d{1,2}-\\d{1,4}

def wrangling_data(df):
    df = df.rename(columns={1: "producto", 3: "precio"})
    df = df[~df.producto.str.contains("CLUBAHORRO|CONSEGUIDOSTOTAL|DESCUENTOS|CONSEGUIDOS|2020",regex=True)]
    df['precio'] = pd.to_numeric(df['precio'],errors='coerce')
    print (df.describe(include='all'))
    df=df.round(2)
    return df

def basic_info(df):
    productosdistintos = len(df.drop_duplicates())
    print('hemos consumido en total: ' + str(productosdistintos) + ' productos distintos')
    dfgb = df.groupby(by='producto').count()
    print("Productos más consumidos: ")
    print(dfgb.sort_values('precio', ascending=False).head())
    print("Productos más caros: ")
    print(df.sort_values('precio', ascending=False).head())
    gastototal=round(df['precio'].sum(),2)
    print("Nos hemos gastado: " +str(gastototal))
    df.to_csv('comidas_clean.csv')
    dfgbsum=df.groupby(by='producto').sum().nlargest(10,'precio')
    print(dfgbsum)
    dfcarne= df[df.producto.str.contains("PAVO|POLLO|CERDO|TERNERA|VACA|LOMO|HAMB|MEAT",regex=True)]
    #print(dfcarne)
    print('en total nos hemos gastado en total en carne: '+str(dfcarne['precio'].sum())+' porcentualmente: '+str(round(dfcarne['precio'].sum()/gastototal,2)))

if __name__ == "__main__":
    df = main()
    df=wrangling_data(df)
    basic_info(df)

# TODO sacar los pdfs del source y meterlos en carpeta data
# TODO extraer los procudtos animales y pescados (REGEX)
# Todo graficar los porcentajes
# Todo automatizar la descarga de los pdfS? y updatear todo?
