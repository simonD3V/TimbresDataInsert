# TimbresDataInsert
Inserting "timbres" data for the musicological database

![Insertion des timbres](https://www.akg-images.co.uk/Docs/AKG/Media/TR5/c/4/1/c/AKG331498.jpg "Insertion des timbres")

## Tâches à réaliser

- [ ] Reproduire le modèle de la base sur _Directus_
  * [Adresse de l'interface _Directus_](http://bases-iremus.huma-num.fr/timbres/admin/login)
  
- [ ] _Normaliser_ les noms des champs de chaque table

- [ ] Ecrire un script python permettant :
  * de générer un token d'identification et de se log sur le projet _Directus_ "Timbres";
  * d'insérer les données via l'API de Directus;
  * de sauvegarder l'id et l'uuid des nouvelles données insérées en format YAML.

