#Author: Reilly, Evan, and Guy
#Class: CS-351
#Purpose: This file will define what the render node 

#import division
from __future__ import division
 
#import Librarys
import numpy as np
import matplotlib.pyplot as plt

#import server stuff
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import socket

#set server settings
node_hostname = socket.gethostname()
control_hostname = node_hostname
render_socket = 1234
control_socket = 5678
control = xmlrpc.client.ServerProxy("http://" + control_hostname + ":" + str(control_socket) + "/")

#Offset of the image
offset = 0.8

#This is the main function of the node
#This function will return a list with two items
#The first item will be the name of the file
#The second item will be the data of the file
def mandelbrot(size, quadrant):
    m = size
    n = size
    Z = np.full((n, m), 0 + 0j)
    s = size - 50

    #Checks to see what quadrant the node is suppose to render
    if(quadrant == "UPPERRIGHT"):
        x = np.linspace(0-offset, (m / s)-offset, num=m).reshape((1, m))
        y = np.linspace(0, n / s, num=n).reshape((n, 1))
        C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
    elif(quadrant == "UPPERLEFT"):
        x = np.linspace((-m / s)-offset, 0-offset, num=m).reshape((1, m))
        y = np.linspace(0, n / s, num=n).reshape((n, 1))
        C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
    elif(quadrant == "LOWERRIGHT"):
        x = np.linspace(0-offset, (m / s)-offset, num=m).reshape((1, m))
        y = np.linspace(-n / s, 0, num=n).reshape((n, 1))
        C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
    elif(quadrant == "LOWERLEFT"):
        x = np.linspace((-m / s)-offset, 0-offset, num=m).reshape((1, m))
        y = np.linspace(-n / s, 0, num=n).reshape((n, 1))
        C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
    else:
        #If this block is tiggered, then the entire Mandelbrot set is generated
        print("ERROR: quadrant's value is not set right")
        x = np.linspace((-m / s)-offset, (m / s)-offset, num=m).reshape((1, m))
        y = np.linspace(-n / s, n / s, num=n).reshape((n, 1))
        C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))

    #The Mandelbrot set is Generated below
    M = np.full((n, m), True, dtype=bool)
    N = np.zeros((n, m))
    for i in range(256):
        Z[M] = Z[M] * Z[M] + C[M]
        M[np.abs(Z) > 2] = False
        N[M] = i
    
    #Return the output of the saveImage function
    return saveImage(quadrant, size, N)

#This Function will save the rendered image as a png file
def saveImage(name, size, colorArray):
    fig = plt.figure()
    fig.set_size_inches(size / 100, size / 100)
    ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.imshow(np.flipud(colorArray), cmap='Spectral')
    plt.savefig(name + '.png')
    plt.close()
    return sendImage(name + '.png')

#This Function will break down the new file into a list with the name and data stored
def sendImage(filename):
    image = open(filename, "rb")
    data = xmlrpc.client.Binary(image.read())
    print("sending file")
    image.close()
    return [filename, data]

#Setting up the node as an RPC server
server = SimpleXMLRPCServer((node_hostname, render_socket))
server.register_function(mandelbrot, "mandelbrot")
server.register_introspection_functions()
server.serve_forever()
