# -*- coding: cp1252 -*-
#*****************************************************************************
# Autor: Pablo Argueta Carné: 13028
# Autor: Héctor Möller: 09002
# Sección: 30
# Fecha: 26/8/14
# Nombre de Archivo: Programa.py
# Breve Descripción: Simulador de un Sistema Operativo con colas por medio de
#                    Simpy.
#*****************************************************************************
import random
import simpy

randomSeed=42	#Random seed para que siempre se genere el mismo patrón de random
cantProcesos=25 #Cantidad de procesos a ejecutar por el Sistema Operativo
intervaloDeProcesos=10 #Generar procesos con este intervalo entre procesos
#Ram es la cantidad de memoria
#Cpu es el recurso para correr los procesos
def source(env,cantProcesos,intervalo,ram,cpu,waiting):
    for i in range(cantProcesos):
        #Se le asigna al proceso una cantidad random de instrucciones entre 1 y 10
        instrucciones=random.randint(1,10)
        #Se le asigna al proceso una cantidad random de memoria ram necesaria entre 1 y 10
        memoria=random.randint(1,10)
        correrProceso=proceso(env,'Número de Proceso: %03d'%i,memoria,ram,cpu,waiting,instrucciones)
        env.process(correrProceso)
        t=random.expovariate(1.0/intervalo)
        yield env.timeout(t)
#Función que corre cada proceso, con cada especificación propia
def proceso(env,noProceso,memoria,ram,cpu,waiting,instrucciones):
	#Variable para llevar control del tiempo de corrida total
    global tiempoTotal
    numInst = 3
    #Variable para el tiempo de llegada del Proceso
    tiempoLlegada=env.now
    print('Momento:  %7.4f , %s, Memoria necesaria: %s, Memoria disponible: %s'%(tiempoLlegada,noProceso,instrucciones,ram.level))
    #Se necesita memoria para pasar a ready
    with ram.get(memoria) as req:
        yield req
    espera=env.now-tiempoLlegada
    print('Momento:  %7.4f , %s, Ready espero ram %6.3f'%(env.now,noProceso,espera))

    #Se ejecuta el proceso, se ejecutan de 3 en 3
    while instrucciones>0:
          #Se necesita usar el cpu
          with cpu.request() as reqCpu:
              yield reqCpu
              print('Momento:  %7.4f , %s, Running instrucciones %6.3f'%(env.now,noProceso,instrucciones))
              yield env.timeout(1) #Tiempo dedicado por el cpu
              #Se le restan las 3 instrucciones procesadas
              if instrucciones>numInst:
                  instrucciones=instrucciones-numInst
              else:
                  instrucciones=0
              #Si aún quedan instrucciones por procesar se decide si pasar a Ready o Waiting
              if instrucciones>0:
                  siguiente=random.choice([0,1])
                  if siguiente==0:
					#Se necesita esperar por I/O
                      with waiting.request() as reqWaiting:
                          yield reqWaiting
                          print('Momento:  %7.4f , %s, Waiting'%(env.now,noProceso))
                          yield env.timeout(1)
                  #Se vuelve a esperar por CPU
                  print('Momento:  %7.4f , %s, Ready'%(env.now,noProceso))
    #Se termina el proceso
    tiempoProceso=env.now-tiempoLlegada
    print('Momento:  %7.4f , %s, Terminated, Tiempo de ejecución %s'%(env.now,noProceso,tiempoProceso))
    #Se regresa la memoria que se utilizó
    with ram.put(memoria) as reqDevolverRam:
        yield reqDevolverRam
        print('Momento:  %7.4f , %s, Regresando Ram %s'%(env.now,noProceso,memoria))
    tiempoTotal = tiempoTotal + (env.now - tiempoLlegada)
#Se configura el ambiente de simulación y se inicializan las variables
print ('Sistema Operativo')
random.seed(randomSeed)
env=simpy.Environment()

#Start processes and run
tiempoTotal = 0
cpu=simpy.Resource(env,capacity=1) #Cantidad de cpu
ram=simpy.Container(env,init=100,capacity=100) #Cantidad de ram
waiting= simpy.Resource(env,capacity=1) #Cola de atencion de I/O
env.process(source(env,cantProcesos,intervaloDeProcesos,ram,cpu,waiting))
env.run()        
print "Tiempo de Ejecución: " , tiempoTotal, ": Promedio del tiempo por Proceso: " , tiempoTotal/cantProcesos
