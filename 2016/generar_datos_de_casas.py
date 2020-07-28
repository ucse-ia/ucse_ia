import random
import pandas as pd


datos = []

for _ in range(100):
    metros = random.randint(50, 400)
    habitaciones = random.randint(3, 10)
    edad = random.randint(1, 100)
    precio = int(200000 + metros * 1000 + random.randint(- metros * 200, metros * 500) * random.random())
    
    datos.append((metros, habitaciones, edad, precio))


df = pd.DataFrame(datos, columns=['metros', 'habitaciones', 'edad', 'precio'])
df.to_csv('casas.csv', index=False)

