#-----------------------------FUNCIONES DE CÁLCULOS Y GRÁFICOS PARA ETL Y EDA--------------------------------




# Importaciones
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns




# FUNCIONES: 

#Verifica el tipo de variable de cada columna.

def verificar_tipo_variable(df):
    mi_dict = {"nombre_campo": [], "tipo_datos": []}

    for columna in df.columns:
        mi_dict["nombre_campo"].append(columna)
        mi_dict["tipo_datos"].append(df[columna].apply(type).unique())
    df_info = pd.DataFrame(mi_dict)
        
    return df_info




#Convierte las variables de una columna de tipo str a tipo tiempo.

def convertir_a_time(x):
    if isinstance(x, str):
        try:
            return datetime.strptime(x, "%H:%M:%S").time()
        except ValueError:
            return None
    elif isinstance(x, datetime):
        return x.time()
    return x




#Verifica y muestra filas duplicadas en un DataFrame basado en una columna específica.

def verifica_duplicados_por_columna(df, columna):
    # Se filtran las filas duplicadas
    duplicated_rows = df[df.duplicated(subset=columna, keep=False)]
    if duplicated_rows.empty:
        return "No hay duplicados"
    
    # se ordenan las filas duplicadas para comparar entre sí
    duplicated_rows_sorted = duplicated_rows.sort_values(by=columna)
    return duplicated_rows_sorted




#Imputa valores faltantes en una columna de un DataFrame con el valor más frecuente.

def ingresa_valor_frecuente(df, columna):
    #Se reemplaza 'SD' con NaN en la columna especificada
    df[columna]=df[columna].replace('SD', pd.NA)
    
    #Verifica el valor más frecuente en la columna
    valor_frecuente= df[columna].mode().iloc[0]
    print('El valor más frecuente de', columna, 'es:', valor_frecuente)

    #Se modifican los valores NaN, con el valor más frecuente
    df[columna].fillna(valor_frecuente, inplace=True)




#Imputa valores faltantes en la columna 'Edad' utilizando la edad promedio según el género.

def ingresa_edad_media_segun_sexo(df):
    #Reemplaza 'SD' con NaN en la columna 'Edad'.
    df['Edad']= df['Edad'].replace('SD', pd.NA)

    #Se calcula el valor promedio de la edad, para cada género(es decir, agrupamos por género).
    promedio_por_genero= df.groupby('Sexo')['Edad'].mean()
    print(f'La edad promedio de Femenino es {round(promedio_por_genero["FEMENINO"])} y de Masculino es {round(promedio_por_genero["MASCULINO"])}')

    #Modificamos los valores NaN en 'Edad', con los valores correspondientes en cada género.
    #Se verifica fila por fila, si el valor en 'Edad' es NaN, se aplica la función, sino se devuelve el valor original.
    df['Edad']= df.apply(lambda row: promedio_por_genero[row['Sexo']] if pd.isna(row['Edad']) else row['Edad'], axis=1)

    #Convertimos el valor ingresado a tipo int
    df['Edad']= df['Edad'].astype(int)




#Devuelve la categoría de tiempo correspondiente a la hora proporcionada.

def crea_categoria_momento_dia(hora):
  if hora.hour >= 6 and hora.hour <= 10:
    return "Mañana"
  elif hora.hour >= 11 and hora.hour <= 13:
    return "Medio día"
  elif hora.hour >= 14 and hora.hour <= 18:
    return "Tarde"
  elif hora.hour >= 19 and hora.hour <= 23:
    return "Noche"
  else:
    return "Madrugada"  



#Devuelve el rango etario correspondiente a una edad.

def rango_etario(edad):
    if edad <= 15:
        return 'Infantes'
    elif edad >= 16 and edad <= 25:
        return 'Jóvenes'
    elif edad >= 26 and edad <= 50:
        return 'Adultos'
    elif edad >= 51 and edad <= 70:
        return 'Adultos mayores'
    else:
        return 'Ancianos'
    



# GRÁFICOS: 

#Crea gráficos de línea para la cantidad de víctimas de accidentes mensuales por año.

def accidentes_mensuales(df):
    # Se obtiene una lista de años únicos
    años = df['Año'].unique()

    # Se define el número de filas y columnas para la cuadrícula de subgráficos
    n_filas = 3
    n_columnas = 2

    # Se crea una figura con subgráficos en una cuadrícula de 2x3
    fig, axes = plt.subplots(n_filas, n_columnas, figsize=(14, 8))

    # Se itera a través de los años y crea un gráfico por año
    for i, year in enumerate(años):
        fila = i // n_columnas
        columna = i % n_columnas
        
        # Se filtran los datos para el año actual y agrupa por mes
        data_mensual = (df[df['Año'] == year]
                        .groupby('Mes')
                        .agg({'Cantidad víctimas':'sum'}))
        
        # Se configura el subgráfico actual
        ax = axes[fila, columna]
        data_mensual.plot(ax=ax, kind='line')
        ax.set_title('Año ' + str(year)) ; ax.set_xlabel('Mes') ; ax.set_ylabel('Cantidad de Víctimas')
        ax.legend_ = None

        # Se personaliza el fondo y el color de la línea del gráfico
        ax.set_facecolor('#FFEBCD')  # Cambia el color de fondo del gráfico
        ax.lines[0].set_color('#B22222')  # Cambia el color de la línea del gráfico
        
    # Se muestra y acomoda el gráfico
    plt.tight_layout()
    plt.show()



#Calcula los meses con más cantidad de accidentes.

def meses_con_mas_accidentes(df):
    # Agrupar por mes y contar la cantidad de accidentes en cada mes
    data_meses = df.groupby('Mes').size().reset_index(name='Cantidad de Accidentes')

    # Ordenar los datos por cantidad de accidentes de manera descendente
    data_meses = data_meses.sort_values(by='Cantidad de Accidentes', ascending=False)

    # Configurar el gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(data_meses['Mes'], data_meses['Cantidad de Accidentes'], color='#8FBC8F')
    plt.title('Meses con Mayor Cantidad de Accidentes')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad de Accidentes')
    plt.xticks(rotation=45)
    plt.grid(axis='y', color='#B22222', linestyle='--', linewidth=0.5)

    # Mostrar el gráfico
    plt.tight_layout()
    plt.show()




#Calcula la cantidad de accidentes por categoría de tiempo y muestra un gráfico de barras.

def cantidad_accidentes_por_categoria_tiempo(df):
    # Convertir la columna 'Hora completa' a tipo datetime si es necesario
    if not pd.api.types.is_datetime64_any_dtype(df['Hora completa']):
        df['Hora completa'] = pd.to_datetime(df['Hora completa'], format='%H:%M:%S').dt.time

    # Se aplica la función crea_categoria_momento_dia para crear la columna 'categoria_tiempo'
    df['Categoria tiempo'] = df['Hora completa'].apply(crea_categoria_momento_dia)

    # Se cuenta la cantidad de accidentes por categoría de tiempo
    data = df['Categoria tiempo'].value_counts().reset_index()
    data.columns = ['Categoria tiempo', 'Cantidad accidentes']

    # Se calculan los porcentajes
    total_accidentes = data['Cantidad accidentes'].sum()
    data['Porcentaje'] = (data['Cantidad accidentes'] / total_accidentes) * 100
    
    # Se crea el gráfico de barras
    plt.figure(figsize=(6, 4))
    ax = sns.barplot(x='Categoria tiempo', y='Cantidad accidentes', data=data, color='#2E8B57')

    ax.set_title('Cantidad de Accidentes por Momento del Día') ; ax.set_xlabel('Categoría de Tiempo') ; ax.set_ylabel('Cantidad de Accidentes')

    # Se agrega las cantidades en las barras
    for index, row in data.iterrows():
        ax.annotate(f'{row["Cantidad accidentes"]}', (index, row["Cantidad accidentes"]), ha='center', va='bottom', color='#B22222')

    # Se agrega el color de fondo al gráfico
    ax.set_facecolor('#FFEBCD')

    # Se muestra el gráfico
    plt.show()




#Genera una tabla que muestra la cantidad de accidentes por día de la semana.

def cantidad_accidentes_por_dia_semana_cuadro(df):
    # Se convierte la columna 'Fecha' a tipo de dato datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    
    # Se extrae el día de la semana (0 = lunes, 6 = domingo)
    df['Dia semana'] = df['Fecha'].dt.dayofweek
    
    # Se crea una columna 'Dia de la semana' para el nombre del día
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    df['Dia de la semana'] = df['Dia semana'].apply(lambda x: dias_semana[x])
    
    # Se cuenta la cantidad de accidentes por día de la semana
    data = df['Dia de la semana'].value_counts().reset_index()
    data.columns = ['Día de la semana', 'Cantidad de accidentes']
    
    # Se ordenan los días de la semana de manera cronológica
    data['Día de la semana'] = pd.Categorical(data['Día de la semana'], categories=dias_semana, ordered=True)
    data = data.sort_values('Día de la semana')
    
    # Mostrar los datos en forma tabular
    print(data)




#Genera un resumen de los accidentes de tráfico por tipo de calle y cruce.

def accidentes_tipo_de_calle(df):
    # Se crea el gráfico
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    
    sns.countplot(data=df, x='Tipo de calle', ax=axes[0], color='#2E8B57')
    axes[0].set_title('Cantidad de víctimas por tipo de calle') ; axes[0].set_ylabel('Cantidad de víctimas')

    sns.countplot(data=df, x='Cruce', ax=axes[1], color='#2E8B57')
    axes[1].set_title('Cantidad de víctimas en cruces') ; axes[1].set_ylabel('Cantidad de víctimas')
    
    # Cambiar color de fondo de los gráficos
    axes[0].set_facecolor('#FFEBCD')  
    axes[1].set_facecolor('#FFEBCD')  
    # Mostramos los gráficos
    plt.show()




#Calcula la cantidad de accidentes por Comuna.

def cantidad_accidentes_por_comuna(df):
    # Se cuenta la cantidad de accidentes por comuna
    data = df['Comuna'].value_counts().reset_index()
    data.columns = ['Comuna', 'Cantidad de accidentes']
    
    # Se ordenan las comunas por la cantidad de accidentes de manera ascendente
    data = data.sort_values('Cantidad de accidentes', ascending=True)
    
    # Mostrar los datos en forma tabular
    print(data)




#Calcula el tipo de vehículo que más accidentes ocasiona.

def cantidad_accidentes_por_tipo_acusado(df):
    # Se cuenta la cantidad de accidentes por tipo de acusado
    data = df['Acusado'].value_counts().reset_index()
    data.columns = ['Tipo de Vehículo', 'Cantidad de Accidentes']
    
    # Se ordenan los tipos de acusado por la cantidad de accidentes de manera descendente
    data = data.sort_values('Cantidad de Accidentes', ascending=False)
    
    # Se crea el gráfico de barras
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='Tipo de Vehículo', y='Cantidad de Accidentes', data=data, color='#8FBC8F')
    
    ax.set_title('Cantidad de Accidentes por Tipo de Vehículo')
    ax.set_xlabel('Tipo de Vehículo')
    ax.set_ylabel('Cantidad de Accidentes')
    
    # Rotación de etiquetas en el eje x para mejor visualización
    plt.xticks(rotation=45, ha='right')
    
    # Se agrega las cantidades en las barras
    for index, row in data.iterrows():
        ax.annotate(f'{row["Cantidad de Accidentes"]}', (index, row["Cantidad de Accidentes"]), ha='center', va='bottom', color='#B22222')
    
    # Se cambia el color de fondo del gráfico
    ax.set_facecolor('#FFEBCD')

    # Se muestra el gráfico
    plt.tight_layout()
    plt.show()

    # # Se calcula la cantidad de acusados
    acusados_counts = df['Acusado'].value_counts().reset_index()
    acusados_counts.columns = ['Acusado', 'Cantidad de acusados']

    # # Se calcula el porcentaje de acusados
    total_acusados = acusados_counts['Cantidad de acusados'].sum()
    acusados_counts['Porcentaje de acusados'] = round((acusados_counts['Cantidad de acusados'] / total_acusados) * 100,2)

    # # Se ordenan los datos por cantidad de acusados en orden descendente
    acusados_counts = acusados_counts.sort_values(by='Cantidad de acusados', ascending=False)
    # # Se imprimen resumen
    print("Resumen de acusados:")
    print(acusados_counts)


#Genera un resumen de la cantidad de víctimas por sexo, rol y tipo de vehículo en un accidente de tráfico.

def cantidad_victimas_sexo_rol_victima(df):
    # Se crea el gráfico
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Gráfico 1: Sexo
    sns.countplot(data=df, x='Sexo', ax=axes[0], color= '#8FBC8F')
    axes[0].set_title('Cantidad de víctimas por sexo') ; axes[0].set_ylabel('Cantidad de víctimas')

    # Se define una paleta de colores personalizada (invierte los colores)
    colores_por_defecto = sns.color_palette("Set2")
    colores_invertidos = [colores_por_defecto[1], colores_por_defecto[0]]
    
    # Gráfico 2: Rol
    df_rol = df.groupby(['Rol', 'Sexo']).size().unstack(fill_value=0)
    df_rol.plot(kind='bar', stacked=True, ax=axes[1], color=['#2E8B57', '#BC8F8F'])
    axes[1].set_title('Cantidad de víctimas por rol') ; axes[1].set_ylabel('Cantidad de víctimas') ; axes[1].tick_params(axis='x', rotation=45)
    axes[1].legend().set_visible(False)
    
    # Gráfico 3: Tipo de vehículo
    df_victima = df.groupby(['Víctima', 'Sexo']).size().unstack(fill_value=0)
    df_victima.plot(kind='bar', stacked=True, ax=axes[2], color=['#2E8B57', '#BC8F8F'])
    axes[2].set_title('Cantidad de víctimas por tipo de vehículo') ; axes[2].set_ylabel('Cantidad de víctimas') ; axes[2].tick_params(axis='x', rotation=45)
    axes[2].legend().set_visible(False)

    # Cambiar color de fondo de los gráficos
    axes[0].set_facecolor('#FFEBCD')  
    axes[1].set_facecolor('#FFEBCD')  
    axes[2].set_facecolor('#FFEBCD')

    # Se muestran los gráficos
    plt.show() 




#Crea una nueva columna llamada 'Rango etario' en el dataframe recibido, 
#y luego crea un gráfico de barras para mostrar la cantidad de víctimas registradas por rango etario.

def victimas_por_rango_etario(df):
    # se crea una nueva columna llamada 'Rango etario'
    df['Rango etario'] = df['Edad'].apply(lambda edad: rango_etario(edad))

    # Se agrupan los registros por rango etario
    grupos = df.groupby('Rango etario')
       
    # Se crea un gráfico de barras
    return grupos['Edad'].size().plot.bar(figsize=(10, 6), color=['#B22222', '#8FBC8F', '#2E8B57', '#E9967A', '#BC8F8F'],
                                           xlabel= 'Rango etario', ylabel='Cantidad de registros')




#Calcula la edad promedio de las víctimas.
def calcular_edad_promedio(df):
    # Verificar que 'Edad' sea numérica para evitar errores
    if pd.api.types.is_numeric_dtype(df['Edad']):
        # Calcular la edad promedio
        edad_promedio = df['Edad'].mean()
        return edad_promedio
    else:
        print("La columna 'Edad' no es numérica.")
        return None  




#Calcula la cantidad de muertes que ocurrieron el mismo día del accidente y la cantidad que ocurrieron luego.

def calcular_muertes_por_tipofecha(df_hechos, df_victimas):
    # Convertir las columnas de fecha a tipo datetime si es necesario
    df_hechos['Fecha'] = pd.to_datetime(df_hechos['Fecha'])
    df_victimas['Fecha fallecimiento'] = pd.to_datetime(df_victimas['Fecha fallecimiento'])

    # Merge de los datasets por las columnas 'Id' y 'Id hecho'
    df_merged = pd.merge(df_hechos, df_victimas, left_on='Id', right_on='Id hecho')
    
    # Filtrar las víctimas que murieron el mismo día del hecho
    mismo_dia = df_merged[df_merged['Fecha fallecimiento'].dt.date == df_merged['Fecha'].dt.date]
    
    # Filtrar las víctimas que murieron en otro día diferente al hecho
    diferente_dia = df_merged[df_merged['Fecha fallecimiento'].dt.date != df_merged['Fecha'].dt.date]
    
    # Contar la cantidad de víctimas en cada grupo
    count_mismo_dia = len(mismo_dia)
    count_diferente_dia = len(diferente_dia)
    
    return count_mismo_dia, count_diferente_dia




#-------------------------------------------------------------------------------------------------------------






