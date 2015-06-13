# Directorio origen de la data
DIRECTORIO_DATA = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/data_estados_financieros/"
DIRECTORIO_CORRELACIONES = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/correlaciones/"

# Lee los nombres de los archivos con la data de los estados financieros
archivos_data = list.files(DIRECTORIO_DATA)

# Se itera sobre cada archivo 
for (archivo in archivos_data){

    empresa = read.table(file=paste(DIRECTORIO_DATA, archivo, sep=""),
                         header=TRUE, sep=",")

    # Se elimina la columna periodo
    empresa = empresa[2:length(empresa)]

    # Crea la matriz de correlaciones
    correlaciones = matrix(data=0, nrow = 17, ncol = 17)

    # Da nombres a las columnas y filas
    # Se lee la data de los estados financieros sin considerar la columna periodo
    # Debido a que en la matriz se utilizan la primera columna y primera fila
    # para colocar los nombres de las variables, se empieza a colocar la data a
    # partir de la segunda columna y fila
    x = 2
    for (name in names(empresa)){
         correlaciones[1,x] = name
         correlaciones[x,1] = name
         x = x + 1
        }

    # Se lee donde terminan los ceros en activos, para saber desde donde se
    # debe empezar a calcular la correlación
    num_activos = 0
    while (empresa[["activos"]][num_activos+1] == 0){
          num_activos = num_activos + 1
    }
    print(num_activos)

    # Se lee donde terminan los ceros en flujo_efectivo
    num_flujo = 0
    while (empresa[["flujo_efectivo"]][num_flujo+1] == 0){
          num_flujo = num_flujo + 1
    }

    # Variables para iterar sobre la matriz correlaciones
    rowcor = 2
    colcor = 2

    # Se calculan las correlaciones
    for (i in 1:length(empresa)){
        # Se reinicia el contador de columnas
        colcor = 2
        for (j in 1:length(empresa)){
            if (correlaciones[rowcor,1] != "flujo_efectivo" && correlaciones[1,colcor] !=
                "flujo_efectivo"){
                   correlaciones[rowcor,colcor] = round(cor(empresa[[i]][num_activos:nrow(empresa)],
                                                   empresa[[j]][num_activos:nrow(empresa)]),2)
            }
            else {
                    correlaciones[rowcor,colcor] = round(cor(empresa[[i]][num_flujo:nrow(empresa)], 
                                                  empresa[[j]][num_flujo:nrow(empresa)]),2)
            }
        colcor = colcor + 1
        }
    rowcor = rowcor + 1
    }

    # Se escribe la matriz de correlaciones en un archivo cuyo prefijo es
    # correlaciones 
    write(correlaciones, file=paste(DIRECTORIO_CORRELACIONES, "correlaciones_",
          archivo, sep=""), ncolumns = ncol(correlaciones), sep=",")
}
