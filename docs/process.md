# Objectif Formule 1

## Sommaire

[TOC]

---

## 1. Introduction

Objectif Formule 1 est un projet qui a pour but de développer un dashboard afin de pouvoir analyser en quelques cliques des données de Formule 1 que ce soit les essais libres, les qualifications, les sprint ou les courses. Une section avec des données globales sur la Formule 1 seront aussi disponible.

De plus des notebooks avec l'analyse de certaines courses seront disponible.

Tout cela a un objectif, c'est de développer mes compétences d'analyse de données de Formule 1 afin de potentiellement pouvoir y travailler un jour.

---

## 2. Déroulé

### A. Récupération des données

Les données proviennent principalement du package Fast-F1 qui s'occupe de faire les différentes requêtes à l'API officielle de la Formule 1 et de Ergast web api.

Le package s'installe avec la commande `pip install fastf1`

D'autres sources seront surement utilisé selon les besoin, avec potentiellement des requêtes directes à l'API de la Formule 1.

### B. Les Technologies

Le projet est en Python 3.9, Python est le principal langage utilisé en data de nos jours, cela paraissait donc être une évidence de l'utiliser.

Pour tout ce qui est récupération des données cela c'est fait en Python via le package `FastF1` qui est le principale package Python pour l'analyse

Pour le traitement de donnée Pandas et Numpy ont été utilisé. L'un est le principal package dans la gestion des Dataframes (modèle de données), l'autre est très utilile pour ce qui est de la gestion des données numérique.

Pour l'affichage des Données nous avons utilisé Dash et Plotly. Pour le dashboard, une multitude de possibilités se proposait à nous mais une chose à fait pencher la balance c'est Plotly, Plotly est une assez grosse librairie basé sur matplotlib plus grosse librairie pour la création de plots. Plotly à l'avantage de créer des plots dynamique et étant développé avec dash cela ouvres des possibilités incroyable tel que des action exécutable lorsque l'on clique sur un plot.

### C. Organisation

![](/assets/images/planning.png)

Le projet suivait son cours et avait même un peu d'avance, malheureusement étant donné que je faisais tout dans le dossier test, dans des notebooks rien n'était push sur Github. Suite à cela de nombreuses choses ont était mise en place tel que le Github mais une grosse perte de motivation et le fait que je n'étais pas chez moi les week-end le projet n'avançait pas beaucoup. De plus j'avais remarqué que lors d'un week-end avec un grand prix j'avais un pic de motivation et le projet avançait plus rapidement.

Etant donné que peu après la perte du projet il y a eu 3 semaines sans formule 1 je me suis concentré sur d'autres chose tel que Dash, de la doc, de la mise en place de sauvegarde sur mon PC, étant donné que je changeais beaucoup de pc et que je n'avais pas forcément de wifi durant les week-ends j'ai transférer mon projet sur un disque au lieu de passé par Github.

---

## 3. Le traitement des données

### A. Leur stockage

Plusieurs options s'offre nous pour l'accès aux données :

1. Via le package sans cache

2. Via le package avec cache

3. Sauvegarder les objets en local

4. Sauvegarder les DataFrames traité

5. Faire un mix

#### 1) Package sans cache

Cette solution permet de charger toutes les données des sessions sans avoir a stocker aucune données en locale.

##### a) Avantages

Prend très peu de place sur la machine et toutes les données de la session sont accessible avec les différents paramètres proposé par le package Fast-F1.

##### b) Inconvénients

Prend beaucoup de temps à charger et nécessite de la bande passante à chaque chargement de la page. Les données peuvent être supprimé après un certain temps.

#### 2) Package avec cache

Cette solution permet de charger toutes les données des sessions avec un temps de chargement un peu plus rapide.

##### a) Avantages

Les données de la session sont accessible avec les différents paramètres proposé par le package Fast-F1, n'utilise pas de bande passante une fois les données ayant été chargé une première fois.

##### b) Inconvénients

Prend beaucoup de place sur le disque, environ 250Mo/Grand Prix, de plus les données reste quand même lente à charger. Les données peuvent être supprimé après un certain temps.

#### 3) Sauvegarder l'objet

Ici on utilise un package comme JobLib pour enregistrer l'objet de la session sur notre disque dur.

##### a) Avantages

Une fois les données téléchargées même si elles sont supprimé de l'API F1 nous pourront toujours aller les chercher. Après avoir été chargé une première fois les données sont très rapide à charger, de plus nous pouvons toujours utiliser les propriétés du package Fast-F1.

##### b) Inconvénients

Ça demande malgré tous beaucoup d'espace disque surtout que de nombreuses données enregistrées ne servent pas pour le moment.

#### 4) Sauvegarder les DataFrames

Pour cette méthode on traite toutes les données chargé afin de les ranger dans des DataFrames.

##### a) Avantages

Les données sont chargé très rapidement une fois qu'elles ont été chargées une première fois. L'espace prit sur le disque est très faible. Les données sont prêtes à être afficher sur les plots.

##### b) Inconvénients

Si on veut faire un nouveau plot nous n'avons pas accès à toutes les données des sessions, ça peut donc nous limiter. Certain DataFrames peuvent-être très gros. Nous n'avons pas l'accès à certain paramètre de Fast-F1. Il faut faire un traitement en amont.

#### 5)Le Mix

Il s'agit ici de faire un mix entre la méthode 3 et la méthode 4.

##### a) Avantages

Les données sont rapide à charger, on peut décider la méthode la plus optimiser pour chacune des sessions. Prend pas trop de place sur le disque entre 80 et 100Mo par Grand Prix

##### b) Inconvénients

Requiert le traitement de certaines données, si on veut ajouter un nouveau plot certaines données peuvent venir à manquer.

##### c) Pourquoi cette méthode

Le choix se portait sur la méthode 4 mais un plot nécessitait de sauvegarder un DataFrame de 70Mo pour chaque course. C'est là que mets venue l'idée de sauvegarder les DataFrames sur les Essais Libres, et Qualifications et pour les sprint et les course de sauvegarder l'objet.

Le DataFrame qui prend énormément de place est celui de la télémétrie de chaque pilote. Pour la course il était nécessaire de sauvegarder la télémétrie pour chaque tour afin de pouvoir comparer les pilotes tour par tour tandis que pour les Essais Libres et les Qualifications ces données ne nous intéressent que pour le meilleur tour de chaque pilote afin de comprendre où il perdent du temps durant leur meilleur tour.

### B. Les DataFrames

#### 1) Les Essais Libres et Qualification

Pour chacune des sessions nous auront ces DataFrames :

* Meteo (Température(Piste et Air), Pluie, Temps (s))

* Laps (Pilotes, Temps (s), LapTime (s), L'équipe, Vitesse (4x), Composé pneu, Nb de tour sur les pneu)

* Tel (Distance, RPM moteur, Throttle, DRS, Brake, DriverNb)**

Seulement les principales variables sont afficher

Ajout d'un fil pour les messages de la direction de course

**Meilleur tour uniquement

#### 2) Sprint et Course

Sauvegarde de l'objet de session afin de pouvoir en faire des analyses très complète.

### C. Valeurs Manquantes

Théoriquement aucune valeur n'est manquante.

Plotly est optimisé pour faire en sorte à ce que si une valeur est manquante lors d'un plot de type line il interrompt la ligne. Des valeurs manquantes sont donc ajouté dans les DataFrames Laps des Essais Libres sur la variable LapTime (s) lorsqu'un tour n'est pas fiable que ce soit parce que le pilote sort/rentre au stand ou fait un tour lent afin de recharger les batteries. Cela fera en sorte à ce qu'on ai pas de valeurs qui dégradent la lecture du plot.

---

## 4. Création des objets

Comme dit précédemment afin d'accélérer le chargement des données, on a mis en place un système où les données sont enregistrées localement.

On a créé une class pour chaque session, lorsqu'elle est initialisée elle va aller chercher la session en question si c'est une Qualification, un Sprint ou une course tout en vérifiant que la session est bien passé. Ensuite nous vérifions si un des fichiers qui est censé être créé au premier chargement de la session est créé. S'il n'est pas créé on va alors chargé la session et traiter les données comme il se doit avant de les enregistrer. Ensuite, ou si le fichier existait, on le charge et on le retourne à l'utilisateur afin qu'il puisse s'en servir.

Pour les essais libres c'est un peu plus complexe, il a fallu décider si on chargeait toutes les sessions en même temps ou une par une. Le choix c'est tourné vers toute en même temps. pour se faire nous avons créer un système pour faire en sorte à ce que si c'est un week-end Sprint (que 2 Essais Libre) on ne récupère que 2 sessions d'Essais Libres tout comme si une seule ou seulement 2 Essais Libres sont passé pour le moment on ne retourne un objet avec que les sessions qui ont pu être chargé et des variable pour signifier que certaine variable ne sont pas encore là pour éviter les erreurs lors de la création des plots. sinon on fait les même vérifications et traitements pour chaque Essai Libre que pour les Qualifications.

---

## 5. Les Plots

### A. Essais Libres

Actuellement 6 graphiques par essais libre sont affiché sur le dashboard. On a :

* Drivers' Laps Time : Un scatter plot avec le temps/tour sur la durée de la session, chaque pilote a une couleur différente.

* Teams Speed Trap : Un violin plot qui représente la vitesse des différentes équipe aux passage de la speed trap à chaque tour.

* Teams Laps Time : Un violin plot qui représente les temps pendant les tours rapides de chaque équipe

* Race Sim : Un scatter plot qui représente le plus long stint de chaque, il représente le temps au tour du pilote sur le nombre de tour sur le pneu.

* Team Top Speed : représente la vitesse maximum de chaque équipe durant la session

* Fastest Lap Comparison : Composé de 7 subplots. Le premier est le delta avec le pilote le plus rapide de la session, les 6 autre viennent de la telemetrie des voitures, on a : La vitesse, les frein, le DRS, les rapports, l'accélération et le RPM. Tous les sous plots sont sur la distance

* Weather : Représentation des conditions météo avec la température de la piste, de l'air au fil de la session, fonctionnel mais pas implémenté, manque condition météo pour qu'il soit utile

### B. Qualifications

Les sessions qualification et sprint shootout sont composées des mêmes graphiques que les essais libres.

### C. Sprint et Course

Pour les course nous avons actuellement 5 plots :

- Drivers' Laps Time : Un scatter plot avec le temps par tour de chaque pilote.

- Teams Speed Trap : Un violin plot qui représente la vitesse des différentes équipe aux passage de la speed trap à chaque tour.

- Teams Laps Time : Un violin plot qui représente les temps pendant les tours rapides de chaque équipe.

- Team Top Speed : représente la vitesse maximum de chaque équipe durant la session.

- Drivers's Gap to Winner : représente l'écart au vainqueur de la course de chaque pilote chaque tour.

- Weather : Représentation des conditions météo avec la température de la piste, de l'air au fil de la session, fonctionnel mais pas implémenté, manque condition météo pour qu'il soit utile

---

## 6. Utilités

### A. Couleurs

Les fonctions drivers_color et team_color sont des fonctions utilisant les même fonctions de FastF1 avec un traitement des variable plus poussé et plus optimal pour le projet afin d'avoir une meilleur lisibilité, le support de listes, une couleur par défaut pour les anciens pilotes/équipes.

### B. Template

Template permet de charger les couleurs par défaut de l'app afin d'avoir des plots unique à notre application

### C. Logo

Logo est une fonction qui permet de mettre un logo au fond des différent plot afin de créer un watermark pour indiquer la source en cas de réutilisation des plots du dashboard.

### D. Time

Time comprend plusieurs fonctions qui permettent de facilement de récupérer la timezone du grand prix afin de pouvoir faire correspondre des horaire de Paris et du grand prix pour éviter certain soucis. Selon le serveur sur lequel le Dashboard est hebergé ce paramètre est facilement modifiable.

### E. Datasets

Fonction qui permet d'obtenir facilement des datasets déjà chargé et mis en forme. Actuellement en développement.

---

## 7. Stratégie

### A. Les Données

Pour les données du modèle j'ai récupéré les grand prix de la saison 2022 de toute les équipes en essais libres et en course sur les différentes composantes de pneu.

### B. Le modèle

Une régression linéaire avec un modifier pour la transformer en polynome du 2nd degré à été appliqué. Avec notamment l'utilisation de OneHotEncoder pour transformer les valeurs textuel en valeur numérique.

### C. Le résultat

C'est un peu décevant, le modèle est assez proche de la réalité sur les premier tours du pneu mais sur la fin de vie est loin de la réalité. Cela est du au fait que les équipes de formule 1 change les pneu avant que le temps au tour soit énormément impacté. 

### D. Point d'amélioration

Essayer de récupérer d'autres données notamment celles de Pirelli et potentiellement de changer comment sont encodé des différents grand prix.

---

## 8. Dashboard

### A. Intro

### B. Parts

### C. Notebooks

---

## 9. La Doc

### A. Dans le code

### B. Youtube
