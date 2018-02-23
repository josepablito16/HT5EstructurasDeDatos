import simpy
import random



#solo necesitamos definir ready. Porque en ready es donde pasa todo. 
def ready(nombre, env, instrucciones_totales,instrucciones_restantes):

    global memoria # :( mala practica, pero ni modo

    memoria=memoria+instrucciones_totales
    print('El proceso #%d esta listo para ser procesado con %d instrucciones' % (nombre, instrucciones_restantes))#ready
    yield env.timeout(5)
    #RUNNING
    print memoria
    with cpu.request() as hola:
        yield hola
        yield env.timeout(10)
        if(instrucciones_restantes>3):
            print('El proceso #%d esta se esta procesando en tiempo %d' % (nombre, env.now))
            flag=random.randint(0,1)
            print memoria
            #WAITING
            if(flag==1): #random entre 1 y 2
                print('El proceso #%d esta esperando entrada/salida en tiempo %d' % (nombre, env.now))
                yield env.timeout(20)
                ready(nombre, env, instrucciones_totales,instrucciones_restantes - 3)
                print memoria
            else:
                ready(nombre, env, instrucciones_totales,instrucciones_restantes - 3)
        else:
            #TERMINATED
            print('El proceso #%d finalizo en tiempo %d'%(nombre,env.now))
            print memoria
            memoria=memoria-instrucciones_totales


# ------------------------------- ENVIRONMENT --------------------------- #


env = simpy.Environment()
cpu= simpy.Resource(env,capacity=1)
memoria=0 #LA MEMORIA ES 0 Y LA ACOMODAMOS A LOS PROCESOS QUE USEN
for i in range(5):
    instrucciones = random.randint(1,10)
    print ('El proceso %d# se ha creado en %d con %d instrucciones' % (i, env.now, instrucciones))
    env.process(ready(i,env,instrucciones,instrucciones))
env.run(until=9999999)