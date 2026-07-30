# Crate — API de gestion de bacs à disques

## Utilisateur
Un DJ qui prepare ses sets.

## Objets
- Track : titre, artiste, bpm, duree_s, genre, deezer_id, cree_le
- Crate : nom, description, owner_id
- User  : email, mot de passe hashe

## Endpoints vises (v1)
POST   /auth/register
POST   /auth/login
GET    /tracks?bpm_min=&bpm_max=&genre=&limit=&offset=
POST   /tracks/import      (depuis une recherche externe)
GET    /search?q=          (proxy vers l'API musicale)
GET    /crates
POST   /crates
GET    /crates/{id}
POST   /crates/{id}/tracks/{track_id}
DELETE /crates/{id}/tracks/{track_id}

## Hors scope v1 (assume-le)
Pas d'upload de fichiers audio, pas de detection de tonalite,
pas de partage entre utilisateurs, pas de front avance.
