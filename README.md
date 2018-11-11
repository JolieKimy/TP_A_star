# A star

Ce TP a été réalisé par Kim Aurore Biloni dans le cadre du cours d'Intelligence Artificielle donné par M. Stefano Carrino à la Haute-Ecole Arc Ingénierie de Neuchâtel durant le semestre d'automne 2018.

## Description

Il consiste à implémenter l'algorithme A* sur des villes et des chemins entre elle afin de trouver le chemine le plus optimale pour aller d'une ville A à une ville B.

## Heuristiques

Afin de mieux comprendre les heuristiques, principe sur lequel se repose l'algorithme. Il a fallu en implémenter 5 différentes. Celles-ci sont les suivantes :

* h0(n) = 0
* h1(n) = "la distance entre n et B sur l'axe de x"
* h2(n) = "la distance entre n et B sur l'axe de y"
* h3(n) = "la distance à vol d'oiseau entre n et B"
* h4(n) = "la distance de Manhattan entre n et B"

La question posée est de savoir quelles heuristiques sont admissible. Pour commencer, un heuristique admissible est une fonction retournant toujours un coût optimiste, c'est-à-dire un résultat toujours inférieur ou égal au résultat réel. De ce fait, on peu conclure que les heuristiques h0, h1, h2, et h3 sont admissibles alors que l'heuristique h4 ne l'est pas.

## Utilisation du fichier TP_A_star.py

Le fichier contient une classe nommée CityNode représentant un ville, ces coordonnées géographiques ainsi les routes et leurs longueurs la reliant à ces différents voisins. Il contient bien entendu l'algorithme A* sous la forme de la fonction `a_star(CityNode, CityNode, heuristic)`.

### Construction des villes

Pour construire les villes, il faut utiliser la fonction `constructCities()` qui lit le fichier `./data/positions.txt` puis retourne un dictionnaire ayant comme clé le nom de la ville et comme valeur l'objet CityNode correspondant. La construction des villes est faite mais elle ne possède encore pour l'instant aucun lien entre elles. Pour se faire, il faut appeler la fonction `linkCities(dict)` avec en paramètre le dictionnaire de CityNode. Cette fonction va lire le fichier `./data/connections.txt` contenant les différentes routes. Il agit directement sur le dictionnaire. Les villes sont donc utilisables juste après.

Pour récupérer un objet CityNode, il suffit donc de le récupèrer dans le dictionnaire avec comme clé le nom de la ville.

### Implémentation d'A*

La fonction implémentant l'algorithme possède la signature suivante:

```python3.6
path, distance, visited = a_star(start_city : CityNode, dest_city : CityNode, heuristic)
```

Elle prend donc en paramètre la ville de départ, la ville de destination ainsi qu'une heuristique.

Les résultats fourni par la fonction sont:

* path : dictionnaire contenant les différents CityNode pour aller de la ville A à la ville B. Pour recontruire le chemin, utiliser la fonction `print_path(path, cityB)` avec le chemin et la ville de destination.
* distance : Distance réelle à parcourir pour aller de la ville A à la ville B.
* visited : le nombre de villes visitées pour trouver le chemin retourné.

## Expérimentations

Après la réalisation de ce TP, différents tests ont été réalisés en se basant sur les questions présentes dans la donnée du TP.

En exécutant le fichier, il va construire les villes, les relier puis utiliser l'algorithme A* entre les villes "Paris" et "Prague" en utilisant chacune des heuristiques. Il utilise aussi la classe Timer pour évaluer la vitesse de l'algorithme. La sortie console affiche donc l'heuristique utilisé, le chemin recherché, le temps de calcul, les villes parcourues, la longueur du parcours et le nombre de villes visitées. Ces informations nous sont utiles pour répondre aux questions suivantes.

### L'influence de l'heuristique choisie sur l'efficacité de l'algorithme

En observant la sortie console, on peut affirmer que le choix de l'heuristique a une réelle influence sur l'efficacité de l'algorithme. h0 et h1 visitent plus de 10 villes, h2 et h3 en visitent 8 et h4 en visite 5.

### Exemple de chemins différents suivant l'heuristique utilisé

L'exemple est celui utilisé justement pour la réalisation de ces tests. On peut observer que les 4 premières heuristiques donnes un chemin passant par "Brussels", "Amsterdam", "Munich" et finalement "Prague" alors que la dernière heurisitique h4 passe par "Hamburg" entre "Amsterdam" et "Berlin".

La raison de cette différence est dû au fait que la cinquième heuristique (h4) est non-admissible. Elle choisira donc un chemin n'étant pas le meilleur pour tous les cas.

### Quelle heuristique utilisé dans un cas réel

Logiquement, pour aller d'un point A à un point B, le mieux est de tirer une droite entre les deux et de prendre le chemin qui s'en rapproche le plus. De ce fait, l'heuristique la plus optimiste et donc la plus admissible est la quatrième (h3) utilisant la distance à vol d'oiseau. On ne peut faire mieux que le chemin direct entre un point A et un point B.