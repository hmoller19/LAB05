#Ejemplo de Simulacion:
#un grupo de carros arrancan al mismo tiempo
#cada carro tiene que recorrer un tiempo (generado al azar)
#     antes de llegar a la meta.

import simpy
from random import uniform, Random

# La clase Car modela el comportamiento de cada carro:
class Car(object):
    def __init__(self,id,driveTime,env):
        self.env = env
        self.name=id
        self.action = env.process(self.carDriving(driveTime))
        
    def carDriving(self,driveTime):
        # El carro arranca su motor, en el tiempo now()
        print "%5.1f %s started (driveTime: %f)" %(env.now,self.name,driveTime)
        # Se simula que el carro usa "driveTime" tiempo
        # para llegar a su destino. Llega en el tiempo env.now
        yield env.timeout(driveTime)
        print "%5.1f %s arrived" %(env.now,self.name)

env = simpy.Environment()#inicar ambiente de simulacion. Tiempo = 0
nrCars=10
azar = Random(12345) #se puede reproducir los mismos numeros al azar

for i in range(nrCars):
    driveTime=azar.uniform(1,90)   #un numero al azar
    id="Car"+ str(i)   #identificacion del carro
    c=Car(id, driveTime, env) #se crea una instancia por cada carro
    
    
    
env.run(until=100) #simular para 100 unidades de tiempo
