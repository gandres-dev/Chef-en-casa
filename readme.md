# Chef en casa

Aplicación de recomendaciones de recetas según tus ingredientes.

## Obtencion de los datos
Utilizando tećnicas de web scraping se obtuvo la informacion del las recetas a traves del sitio https://recetas-mexicanas.com.mx/, se guardo la informacion en MongoDB dado que las recetas no tiene un esquema fijo, dado que puede tener varios ingredientes y son extraidos en un formato json.

![scraper](img/demo-craper.gif)



## Diseño algoritmico

No siempre la mejor receta será la que tiene exactamente los mismos ingredientes, ya que puede existir la posibilidad de que no sea apetitosa la receta recomendada, por lo que es mejor tener diferentes opciones, por supuesto, estas diferentes opciones tienen que tener ingredientes que tengas a la mano. A partir de esto se puede generar un Heap que es un arbol binario completo que se formara a partir de las coincidencias de los ingredientes y de esta forma recomdar más recetas según tus ingredientes.

