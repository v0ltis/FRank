# Messages de niveau personalisé FRank:


**Vous devez avoir les permissions d'administrateur sur le serveur pour avoir accès à cette commande**
``@FRank setMessage [message]``.

Votre message peut être simplement "Un utilisateur a gagné un niveau", mais également "@FRank vient de gagner un niveau. Il est désormais à la 7e place sur 653 participants."


### Voici la liste d'arguments possibles:

|Arguments|Valeur|Exemple|
|---|----|-----|
|userName|Nom d'utilisateur|Frank
|userDiscrim|nombres après le # de l'utilisateur| 7228 
|userId|Id de la personne | 738341837395197952
|userMention|Mention de la personne| @FRank#7228
|guildName|Nom du serveur|FRank's serveur
|guildId|Id du serveur|573909687704092673
|guildMemberCount|Nombre de membres sur le serveur|81
|channelId|ID du salon où le niveau à été gagné| 691630212084924446
|ChannelName|Nom du salon où le niveau a été gagné| général
|ChannelMention|Mention du salon où le niveau a été gagné| #général
|second|Seconde où le niveau à été gagné| 18
|minute|minute où le niveau à été gagné| 36
|hour|Heure où le niveau à été gagné| 12
|intDay|Jour (en chiffre) où le niveau a été gagné| 28
|intMonth|Mois (en chiffre) où le niveau a été gagné| 12
|year|Année où le niveau a été gagné|2020
|strDay|Jour (en texte) où le niveau a été gagné| Lundi
|strMonth|Mois (en texte) où le niveau a été gagné| Décembre
|userLevel|Nouveau niveau du membre| 25
|oldUserLevel|Ancien niveau du membre| 24
|userRank|Position dans le classement de la personne|3
|userRanked|Nombre de personnes dans le classement|
|NextLevelNeedXp|Nombre d'xp à optenir pour accéder au prochain niveau|
Et bientôt d'autres ...

### Comment utiliser la commande:
``@FRank setMessage [message]``.
Par exemple:

``@FRank setMessage Bravo {.userMention}, tu es désormais niveau {.userLevel}! Il te faut {.NextLevelNeedXp} xp pour acceder au prochain niveau !``
affichera:
``Bravo @FRank#7224, tu es désormais niveau 7! Il te faut 422 xp pour acceder au prochain niveau, bonne chance !``


Il y a une limite de 1000 caractères, pour eviter tout spam.

**Cette commande est résérvée aux modérateurs.**
--------------------------
