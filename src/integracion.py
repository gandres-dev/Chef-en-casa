"""Capa de integracion"""

#Esta sera la capa de integracion con la cual se conectara la base de datos y
#obtendra toda la informacion necesaria para poder pasarsela a la capa de modelo la
#cual contendra toda la logica que seria la capa del Negocio

import pickle #Libreria para serializar objetos
from arbol import Arbol
from pymongo import MongoClient

import os

from receta import Receta

def obtenerReceta(ruta):
	"""Obtene la receta de un archivo serializado
	
	Parametros
	----------
	ruta: str
		Ruta donde se encuentra la receta serializada.
	"""
	try:
		archivo = open(ruta, "rb" )
		# Desarealizamos nuestro objeto receta.
		receta = pickle.load(archivo)
		#archivo.close()
	except:
		print("No se pudo encontrar el archivo")
		#archivo.close()
	#print(receta)
	return receta


def obtenerRecetario(use_db=False):
	'''Carga todas las recetas en memoeria a traves de un archivo txt.

	Para obtener todo el recetario necesitamos cargar todo las recetas en la memoria y conservar su contenido hasta
	que se finalize el programa por lo tanto se necesitara una estructurda datos en cual podamos almacenar nuestra 
	informacion de manera organizada para puedan ser utlizados de manera eficiente 
	Utilizaremos una estructuras  de  datos  no  lineales  o estructuras multi-enlazadas que pueden presentar
	relaciones más complejas entre los elementos, la cual será un arboles binarios de busqueda.

	Retorna
	-------
	arbolRecetas: 
		Devuelve un estructura de datos arbol que contendra todas las recetas.		
	'''
	if use_db:
		return obtener_recetarioDB()

	with open('baseDatosRecetas/recetario.txt', 'r', encoding='cp1252') as recetario:

		nombreReceta = recetario.readline()
		lista = []
		arbolRecetas = Arbol()
		#Una cadena vacia lo representa como Falso
		while (nombreReceta): 
			#print(nombreReceta)
			ruta = 'baseDatosRecetas/' + nombreReceta.replace("\n","") + ".txt" #quitamos el salto de linea
			#print(ruta)
			#Como ejemplo ulizaremos un lista para probar algunas funcionalidades
			receta = obtenerReceta(ruta)
			# print(type(receta))
			# print(receta)
			#lista.append(receta)
			arbolRecetas.agregar(receta)
			nombreReceta = recetario.readline()		
	
	return arbolRecetas


def obtener_recetarioDB(host='localhost', port=27017):	
	"""Obtener las recetas de la base de datos para cargar en memomria
	
	Parametros
	----------
	host: str
		Direcciones donde se encuentra la base de datos.
	port: int
		Puerto donde se escuha la base de datos.
	"""
	client = MongoClient(host, port)
	db = client['chef-casa']
	recipes_collection = db['recipes']	
	arbolRecetas = Arbol()
	for recipe in recipes_collection.find():		
		receta = Receta(recipe['title'])
		receta.agregar_ingredientes(*recipe['ingredients'])
		receta.agregarPreparacion(recipe['procedimiento'])		
		arbolRecetas.agregar(receta)
	return arbolRecetas


def obtenerArchivoRecetario():
	'''
	Obtiene el archivo llamado recetario.txt que contiene el nombre de las recetas
	@return Devolvera una lista con los nombres de la recetas
	'''
	listaNombresRecetas = []

	try:
		archivo = open('baseDatosRecetas/recetario.txt', 'r')
		nombreReceta = archivo.readline()
		while nombreReceta:
			#print(nombreReceta.replace("\n",""))
			listaNombresRecetas.append(nombreReceta.replace("\n",""))
			nombreReceta = archivo.readline()
			pass
		archivo.close()
	except:
		print("No se pudo abrir")
		archivo.close()

	return listaNombresRecetas
	

def ajustarArchivoRecetario(recetarioNuevo):
	'''
	@param recetarioNuevo sera una lista con el numero recetario
	Modificara el archivo recetario.txt con el recetarioNueco ya que si se 
	elimina una receta, se debe modificar el recetario
	'''
	try:
		archivo = open('baseDatosRecetas/recetario.txt', 'w')
		for receta in recetarioNuevo:
			archivo.write(receta + '\n')
		
		archivo.close()
	except:
		print("No se pudo abrir el archivo")
		archivo.close()

	pass

def eliminarReceta(nombreReceta):
	'''
	@parama nombreReceta sera un String que sera el nombre de la receta
	Buscara la receta con respecto a su nombre y la eliminara
	'''
	ruta = "baseDatosRecetas/" + nombreReceta + ".txt"

	if os.path.exists(ruta):
		os.remove(ruta)
	else:
		print("The file does not exist")
	pass

#obtenerReceta("baseDatosRecetas/Sopadecaracol.txt")

#recetario = obtenerRecetario()
#for receta in recetario:
#	print(receta)

#mi_arbol = Arbol()
#recetario = obtenerRecetario()
#Recetario es un arbol
#recetario.imprimirInorden()
#recetario.inorden(recetario.obtenerRaiz(), ["sal".upper()])
#recetario.mostrarCoincidencias()

