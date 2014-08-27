# -*- coding: cp1252 -*-
#*****************************************************************************
# Autor: Pablo Argueta Carné: 13028
# Autor: Héctor Möller: 1
# Sección: 30
# Fecha: 26/8/14
# Nombre de Archivo: Programa.py
# Breve Descripción: Simulador de un Sistema Operativo con colas por medio de
#                    Simpy.
#*****************************************************************************
import random
import simpy

RANDOM_SEED=42
NEW_PROCESS=5 #Cantidad de procesos
INTERVAL_PROCESS=10.0 #Generar procesos con este intervalo entre procesos
def source(env,number,interval,RAM,CPU,WAITING):
    #Source genera procesos al azar, de acuerdo a una distribución exponencial
    #   de acuerdo al intervalo recibido
    #RAM: es el recurso de memoria que se emplea para que el proceso tome
    #   la memoria que necesita
    #CPU: es el recurso de memoria que signa el CPU para correr al proceso
    for i in range(number):
        #Cada proceso tiene un numero al azar de instrucciones a ejecutar
        instrucciones=random.randint(1,10)
        #Cada proceso necesita cantidad de memoria RAM
        memoria=random.randint(1,10)
        c=proceso(env,'ID%03d'%i,memoria,RAM,CPU,WAITING,instrucciones)
        env.process(c)
        t=random.expovariate(1.0/interval)
        yield env.timeout(t)
        
def proceso(env,processID,memoria,RAM,CPU,WAITING,instrucciones):
    #El proceso pasa por todas sus etapas, y luego termina su ejecución
    arrive=env.now
    print('%7.4f %s: NEW (esperando RAM %s), RAM disponible %s'%(arrive,processID,RAM))

    #Estamos en NEW y se necesita memoria para pasar a READY
    with RAM.get(memoria) as req:
        yield req #Esperar por memoria RAM
    wait=env.req-arrive
    print('%7.4f %s: READY espero RAM %6.3f'%(env.now,processID,wait))

    #Se ejecuta el proceso, mientras tenga instrucciones por ejecutar
    while instrucciones>0:
          #Estamos en READY y se necesita utilizar un CPU
          with CPU.request() as reqCPU:
              yield reqCPU #Esperamos por CPU
              print('%7.4f %s: RUNNING instrucciones %6.3f'%(arrive,processID))
              yield env.timeout(1) #Tiempo dedicado por el CPU
              #Disminuye el tiempo por el CPU e Instrucciones faltantes
              if instrucciones>3:
                  instrucciones=instrucciones-3
              else:
                  instrucciones=0

              #Se terminó el tiempo que el CPU dedico a este proceso
              #Si aún existe instrucciones a realizar pasar a READY O WAITING
              if instrucciones>0:
                  siguiente=random.choice(["ready","waiting"])
                  if siguiente=="waiting":
                      with WAITING.request() as reqWAITING:
                          yield reqWAITING #Esperar por I/O
                          print('%7.4f %s: WAITING'%(env.now,processID))
                          yield env.timeout(1) #Tiempo dedicado a hacer I/O
                  #Ahora se pasa a hacer nuevamente cola para esperar a CPU
                  print('%7.4f %s: READY'%(env.now,processID))
    #Se termina el proceso
    tiempoProceso=env.now-arrive
    print('%7.4f %s: TERMINATED tiempo ejecucion %s'%(env.now,processID,tiempoProceso))
    #Regresar la memoria
    with RAM.put(memoria) as reqDevolverRAM:
        yield reqDevolverRAM   #Se regresa la memoria utilizada
        print('%7.4f %s: Regresando RAM %s'%(env.now,processID,memoria))
#Setup and start the simulation
print ('Sistema Operativo')
random.seed(RANDOM_SEED)
env=simpy.Environment()

#Start processes and run
CPU=simpy.Resource(env,capacity=1) #Cantidad de CPU
RAM=simpy.Container(env,init=100,capacity=100) #Cantidad de RAM
WAITING= simpy.Resource(env,capacity=1) #Cola de atencion de I/O
env.process(source(env,NEW_PROCESS,INTERVAL_PROCESS,RAM,CPU,WAITING))
env.run()        
