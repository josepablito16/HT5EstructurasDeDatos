# HOJA 5 - SIMULACIONES

import simpy
import random


# sergio marchena 16387



#solo necesitamos definir ready. Porque en ready es donde pasa todo. 
def ready(nombre, env, instruc,resInstruc):

    global memoria # :( mala practica, pero ni modo

    memoria=memoria+instruc
    print('El proceso #%d esta listo para ser procesado con %d instrucciones' % (nombre, resInstruc))#ready
    yield env.timeout(5)
    #RUNNING
    with cpu.request() as hola:
        yield hola
        yield env.timeout(10)
        if(resInstruc>3):
            print('El proceso #%d esta se esta procesando en tiempo %d' % (nombre, env.now))
            flag=random.randint(0,1)
            #WAITING
            if(flag==1): #random entre 1 y 2
                print('El proceso #%d esta esperando entrada/salida en tiempo %d' % (nombre, env.now))
                yield env.timeout(20)
                ready(nombre, env, instruc,resInstruc - 3)
            else:
                ready(nombre, env, instruc,resInstruc - 3)
        else:
            #TERMINATED
            print('El proceso #%d finalizo en tiempo %d'%(nombre,env.now))
            memoria=memoria-instruc


# ------------------------------- ENVIRONMENT and VARIABLES --------------------------- #

# memoria, capacity, instrucciones, etc.

env = simpy.Environment()
cpu = simpy.Resource(env,capacity=1)
memoria = 0 #LA MEMORIA ES 0 Y LA ACOMODAMOS A LOS PROCESOS QUE USEN

for i in range(5):
    instrucciones = random.randint(1,10)
    print ('El proceso %d# se ha creado en %d con %d instrucciones' % (i, env.now, instrucciones))
    env.process(ready(i,env,instrucciones,instrucciones))
env.run(until=100000)
