# -*- coding: cp1252 -*-
import simpy
import random

# el proceso car muestra un vehículo que se estaciona un tiempo
# y luego se conduce otro lapso de tiempo
def car(nombre,env):
    while True:
        parking_duration = random.randint(1,5)
        print(nombre, 'Start parking at %d' % env.now,' tiempo a estar parkeado ',parking_duration)
        yield env.timeout(parking_duration)

        trip_duration = random.randint(1,2)
        print(nombre,'Start driving at %d' % env.now,' tiempo a conducirse ',trip_duration)
        yield env.timeout(trip_duration)


env = simpy.Environment() #ambiente de simulación
# dos vehículos que se estacionan y luego se conducen por un tiempo
env.process(car('a',env))
env.process(car('b',env))
env.run(until=15)  #correr la simulación hasta el tiempo = 15
