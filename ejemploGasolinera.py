# -*- coding: cp1252 -*-
import simpy
import random

# el proceso car muestra un vehículo que se estaciona un tiempo
# y luego se conduce otro lapso de tiempo

def proceso(nombre,env,driving_time,bomba):

    global totalDia  # :( mala practica, pero ni modo

    # Simular que esta conduciendo un tiempo antes de llegar a la gasolinera
    yield env.timeout(driving_time)
    
    # llegando a la gasolinera
    horaLlegada = env.now

    # simular que necesita un tiempo para cargar gasolina. Probablemente
    # si es carro pequeño necesita menos tiempo y si es carro grande mas tiempo
    tiempoGas = random.randint(1, 7)
    print ('%s llega a las %f necesita %d para hechar gasolina' % (nombre,horaLlegada,tiempoGas))
    
    # ahora se dirige a la bomba de gasolina,
    # pero si hay otros carros, debe hacer cola
    with bomba.request() as turno:
        yield turno      #ya puso la manguera de gasolina en el carro!
        yield env.timeout(tiempoGas) #hecha gasolina por un tiempo
        print ('%s sale de gasolinera a las %f' % (nombre, env.now))
        #aqui el carro hace un release automatico de la bomba de gasolina
        
    tiempoTotal = env.now - horaLlegada
    print ('%s se tardo %f' % (nombre, tiempoTotal))
    totalDia = totalDia + tiempoTotal
           

# ----------------------

env = simpy.Environment() #ambiente de simulación
bomba = simpy.Resource(env,capacity = 2)
random.seed(10) # fijar el inicio de random

totalDia = 0
for i in range(5):
    env.process(proceso('proceso %d'%i,env,random.expovariate(1.0/10),bomba))

env.run(until=50)  #correr la simulación hasta el tiempo = 50

print ("tiempo promedio por proceso es: ", totalDia/5.0)
