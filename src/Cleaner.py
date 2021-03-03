import os
import index as ind

path1 = ind.app.config['UPLOAD_FOLDER']
path2 = ind.app.config["TEMP_DATA"]
path3 = ind.app.config["CLIENT_CSV"]
Plots = ind.app.config["STATIC"]
PLOTHPATH = os.path.join(Plots, "Modelsplot.png")
for filename in os.listdir(path1):
#    #Archivo = table_list.append(filename)
    pathname1 = path1 +"/" +str(filename)
    os.remove(pathname1)
    print("Archivo removido!")

for filename in os.listdir(path2):
#    #Archivo = table_list.append(filename)
    pathname2 = path2 +"/" +str(filename)
    os.remove(pathname2)
    print("Json removido!")

for filename in os.listdir(path3):
#    #Archivo = table_list.append(filename)
    pathname3 = path3 +"/" +str(filename)
    os.remove(pathname3)
    print("CSV removido!")

os.remove(PLOTHPATH)