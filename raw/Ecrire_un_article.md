# Écrire un article de wiki

# categories:guide

Dans ce guide, nous verrons comment écrire un article de wiki, comment le structurer et le mettre en forme. Pour cela, nous utiliserons la syntaxe [Markdown](https://www.markdownguide.org/ "new:Accueil du site officiel"), ce qui permet de rédiger plus rapidement et plus facilement qu'en [HTML](https://fr.wikipedia.org/wiki/Hypertext_Markup_Language "new:HyperText Markup Language - Langage de balisage"), la syntaxe utilisée traditionnellement pour les sites internet.

## Écrire un article

### Que mettre dans un article ?

Un article de wiki est un article qui présente un évènement, une entité, un thème ou une information. Quelque soit le contenu, le sujet abordé est le cœur de la page, et les informations énoncées doivent toujours avor un rapport avec le sujet d'origine. Il peut être écrit par n'importe qui, et peut être modifié par n'importe qui, sous réserve de validation par l'administration du serveur et de l'auteur original. Il peut être court ou long, et peut contenir pour l'instant que du texte et des liens.

L'objectif d'un article de wiki est de présenter un sujet de manière claire et concise, et de fournir des informations utiles à la compréhension du sujet. Il doit être écrit de manière à ce que n'importe qui puisse le comprendre, et doit être structuré afin que l'on puisse facilement trouver l'information recherchée. Le style de rédaction devrait être neutre et éviter les jugements de valeur, mais il peut être personnel et subjectif dans notre cas, étant donné la nature du wiki.

### Comment écrire un article ?

Vous devez donc avoir les différentes parties de votre article en tête, et les rédiger dans un fichier texte. Pour cela, vous pouvez utiliser un éditeur de texte comme [Notepad++](https://notepad-plus-plus.org/ "new:Éditeur de texte gratuit et léger"), qui permet de colorer la syntaxe Markdown et de voir en temps réel le rendu de l'article. Vous pouvez tout à fait vous contenter de l'éditeur de texte de base de votre ordinateur, l'essentiel est d'enregistrer le tout dans un fichier texte, et non pas dans un fichier Word ou autre.

## Le Markdown

> Le formatage du texte avec le Markdown peut se révéler complexe. Totalement facultative, la partie suivante abordera la mise en forme du texte. Si vous avez des difficultés, vous pouvez tout à fait vous contenter d'écrire votre article que nous mettrons en forme par la suite.
>
> Dans ce cas, vous pouvez rédiger votre article avec un traitement de texte. Nous vous demandons également de bien définir vos parties et sous-parties accompagnées de leurs titres.

### Qu'est-ce que le Markdown ?

Le Markdown est une syntaxe de balisage qui permet de mettre en forme du texte. Il est utilisé par de nombreux sites internet, dont GitHub, et permet de rédiger plus rapidement et plus facilement qu'en HTML, la syntaxe utilisée traditionnellement pour les sites internet. Il est très simple à apprendre, et il est possible de trouver de nombreux tutoriels sur internet. Son principe est simple : il suffit d'entourer le texte à mettre en forme avec des caractères spéciaux, comme des astérisques ou des crochets.

Pour commencer, il faut enregistrer votre fichier avec l'extension `.md` (pour **M**ark**d**own). D'habitude, un fichier texte s'enregistre au format `.txt`. Pour un article appelé par exemple *Alféa*, le nom du fichier devrait être `Alféa.md`. Il existe plusieurs façons de mettre en forme son texte, mais ici nous allons voir celles qui nous intéressent.

### Comment styliser son texte ?

#### Styles de base

|    Style   |         Format        |        Rendu        |
|------------|-----------------------|---------------------|
| Italique   | `Texte en *italique*` | Texte en *italique* |
| Gras       | `Texte en **gras**`   | Texte en **gras**   |
| Barré      | `Texte ~~barré~~`     | Texte ~~barré~~     |

#### Les titres

Vous pouvez définir des titres de parties à l'aide de croisillon, ou hashtag en bon anglais. Le nombre de `#` détermine le niveau de titre ; on peut alors obtenir des titres de niveau 1 jusqu'à 6. Par exemple, `## Histoire` fera un excellent titre de niveau 2 (un sous-titre, quoi) si vous avez déjà un titre de niveau 1 tel que `# Alféa`.

```markdown
# Titre de niveau 1

## Titre de niveau 2

### Titre de niveau 3
```

# Titre de niveau 1

## Titre de niveau 2

### Titre de niveau 3

---

#### Les citations

Vous pouvez également définir des citations à l'aide de chevrons. Le style de la citation est similaire à celui utilisé par Discord.

```markdown
> Ceci est une citation
```

> Ceci est une citation

---

#### Les listes à puces

Vous pouvez définir des listes à puces à l'aide de tirets, d'étoiles ou autres.

```markdown
* Élément 1
* Élément 2
* Élément 3
    - Élément 3.1
    - Élément 3.2
    - Élément 3.3
* Élément 4
```

* Élément 1
* Élément 2
* Élément 3
    - Élément 3.1
    - Élément 3.2
    - Élément 3.3
* Élément 4

---

##### Les liens

Vous pouvez définir des liens à l'aide de crochets et de parenthèses. Le texte entre crochets est le texte du lien, et le texte entre parenthèses est l'URL du lien.

Par exemple, le texte `[Wiki Winx Club](https://winx.fandom.com/fr/wiki/Wiki_Winx "Fandom Winx Club")` donnera le lien [Wiki Winx Club](https://winx.fandom.com/fr/wiki/Wiki_Winx "Fandom Winx Club") (vous pouvez passer la souris sur le lien pour voir le texte entre guillemets apparaître).

### Un exemple de mise en forme

Le bloc de texte ci-dessous donne l'article de wiki que vous pouvez trouver [ici](a-nka.github.io/wiki/Exemple.html "Exemple de mise en forme"). L'exemple est volontairement très simple, mais il vous donne une idée de ce que vous pouvez faire avec le Markdown, et est représentatif d'un article typique du wiki.

```markdown

# Alféa

**Alféa** est un lycée magique célèbre dans l'*Autre Monde*. Il est situé dans le royaume de *Solaria*, et il est réputé pour la qualité de son enseignement.

## Description

**Alféa** est un lycée qui enseigne la magie à des fées. Il est situé quelque part dans le monde des Winx, mais on ne sait pas où exactement. Son équipe enseignante vient de tous les horizons, et chaque professeur est réputé dans son propre domaine. Le nombre d'étudiants atteint parfois plusieurs centaines, et tout les types de magies se confondent.

## Histoire

L'histoire exacte du bâtiment est inconnue. On sait seulement qu'il a été longuement utilisé comme lycée, mais il a pu être construit dans un but résidentiel en premier lieu. Situé en plein royaume solarien, il est possible qu'il ait un rapport avec la famille royale. L'origine sans doute [mystique](https://www.cnrtl.fr/definition/mystique "Défition de mystique") d'**Alféa** est aussi fortement mis en valeur par la présence de nœuds de flux magique très importants à proximité du bâtiment.

## Personnages

### Professeurs réputés

* Farah Dowling
* Saul Silva
* Ben Harvey

### Étudiants

* Fées du feu
    - Hope Mikaelson
    - Bloom Peters
* Fées de la terre
    - Terra Harvey
    - Sam Harvey

```

## Informations complémentaires

Toutes les possibilités qu'offre le Markdown ne sont pas abordées ici, et ne sont pas encore toutes supportées par le wiki. Si vous souhaitez en savoir plus, vous pouvez consulter la [documentation officielle](https://www.markdownguide.org/ "new:Documentation officielle du Markdown") pour suggérer des améliorations, ou consulter la page [À propos](/wiki/about.html "À propos") du wiki pour en savoir plus sur les améliorations à venir.