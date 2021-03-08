# TimbresDataInsert
Insertion des données timbres dans la base de données

![Insertion des timbres](https://www.akg-images.co.uk/Docs/AKG/Media/TR5/c/4/1/c/AKG331498.jpg "Insertion des timbres")

## Tâches à réaliser

- [x] Reproduire le modèle de la base sur _Directus_
  * [Adresse de l'interface _Directus_](http://bases-iremus.huma-num.fr/timbres/admin/login)
  
- [ ] _Normaliser_ les noms des champs de chaque table

- [ ] Mettre à jour [la feuille de calcul temporaire](https://docs.google.com/spreadsheets/d/1NA8yjzQz-Q-OSUN7rLpyAC3FK2KHK5r_/edit#gid=808619991)

- [ ] Ecrire un script python permettant :
  * de générer un token d'identification et de se log sur le projet _Directus_ "Timbres";
  * d'insérer les données via l'API de Directus;
  * de sauvegarder l'id et l'uuid des nouvelles données insérées dans un document YAML.

- Demander à Alice de normaliser les identifiants des airs (234 et *234, trois occurrences de 237, deux occurrences de 189…)