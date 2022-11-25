# INSTRUCCIONS PER EXECUTAR EL PROGRAMA

## CREAR L'IMATGE DE DOCKER

Per fer-ho cal executar la següent comanda:

```
docker build . -t shape_recognizer
```

## EXECUTAR EL PROGRAMA

Primer de tot cal executar la imatge: 
```
docker run -it shape_recognizer bash
```
Dins del bash del docker cal instal·lar primer opencv:
```
apt install libopencv-dev python3-opencv
```
(Geographic area: Europe, Time zone: Madrid)

Finalment, podem executar el script dins del docker. El programa només rep un argument, el path de l'imatge a processar. 
Per exemple, per executar test1.png, s'ha d'executar la comanda:
```
python3 shape_recognizer.py ./images/test1.png
```
El resultat tarda uns minuts i apareix en el següent format:
```
Classificació:
----------- COLOR ------------
Vermelles:        29
Verdes:           36
Blaves:           25
----------- FORMES -----------
Triangles:        20
Quadrats:         20
Rectangles:       30
Cercles:          20
------ LOGOS LLEIDAHACK ------
Logos:            7
```
