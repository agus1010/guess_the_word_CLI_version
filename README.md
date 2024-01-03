<h1>¡Adivina la Palabra! (Versión CLI)</h1>


<h3>¿Cómo se juega?</h3>
 
 El objetivo del juego es averiguar la palabra secreta antes de que se
acaben los intentos.
 Para ello el jugador deberá arriesgar una palabra del diccionario español y
de la misma longitud que la palabra secreta.
 Por cada intento, el juego mostrará información sobre cada letra de la palabra
arriesgada en forma de colores, que ayudarán a descubrir la palabra final.
 Los colores indican:
  • <bold>VERDE</bold> : La letra está presente en la palabra final y está en la posición correcta.
  • <bold>AMARILLO</bold> : La letra está presente en la palabra final pero en la posición equivocada.
  • <bold>GRIS</bold> : La letra no está presente en la palabra final.

Por defecto:
 Las palabras secretas pertenecen al diccionario español, no tienen acentos y tienen 5 letras.
 El jugador tiene un total de 6 intentos.

Todos los valores anteriores pueden personalizarse, de forma que:
  • Se permitan palabras secretas con acento.
  • La palabra secreta tenga entre más de 5 (pero menos de 11) letras.
  • El total de intentos sea cualquier número

(mire "wordgame help")


<h3>USO:</h3>
  Para iniciar el juego en modo "estándar":
        python wordgame.py
    
  El modo "estándar" consiste en adivinar una palabra de 5 letras sin acentos en 6 intentos.


<h3>INSTALACIÓN</h3>
pip install requirements.txt