# poethu

poethu is a simple Python library that makes easy to access data from [poet.hu](https://www.poet.hu)

To access the API first you need to [register](https://www.poet.hu/regisztracio.php) on the site.

### Installation (pypi)
```bash
pip install poethu
```
### How to install?
First you need to install Python, if it is not installed it will won't work.

[Download Python](https://www.python.org/downloads/)

```bash
# Ubuntu / Debian
$ sudo apt install python

# Fedora
$ sudo dnf install python
```

Download required packages:
```bash
$ pip install requests
```

### How to use?
Using poethu is very easy.
First you need to register to the site to get the key.
You can do it [here](https://www.poet.hu/regisztracio.php).
After you succesfully registered you can get your key [here](https://poet.hu/api.php)

![image](https://github.com/BXn4/poethu/assets/78733248/2dfdc088-2be4-42f8-82db-f27c2072e32a)

### Usage:
Note: the synonyms and poems returns as a list If you want more than 1 synonyms or poems.
```python
import poethu

poet = poethu.API(username="your_username", password="your_key")
```

#### To get synonyms:
```python
synonyms = poet.get_szinonima(word="Helló") # Change the word to anything else to get the word synonym
print(synonyms)
```
You can easily change the order, or change the max synonym:
```python
synonyms = poet.get_szinonima(word="Helló", order="desc", max=10) # order by desc, and max 10 synonym
print(synonyms)
```

#### And for poems:
```python
poems = poet.get_versek(category="kedvesemnek", max=2)
# The output is raw, so we need to format it.

# You only need to use loops when you want to get more poems than 1
# If you not, you can simply use title = poet.get_title(poems)

for i in range(len(poems)):
    title = poet.get_title(poems)[i]
    text = poet.get_text(poems)[i]
    poem = poet.get_text(poems)[i]
    author = poet.get_author(poems)[i]
    category = poet.get_category(poems)[i]
    favs = poet.get_favs(poems)[i]
    id = poet.get_id(poems)[i]
    url = poet.get_url(poems)[i]

    print(f"Title: {title}")
    print(f"Text: {text}")
    print(f"Author: {author}")
    print(f"Category: {category}")
    print(f"Favs: {favs}")
    print(f"ID: {id}")
    print(f"url: {url}")
```
Poem params:
```
category
author
text
max (number)
order_by (id, ido, szerzo, kedvencek, veletlen)
order (asc, desc)
continue_from (number)
```
You can get more information about the API [here](https://www.poet.hu/api.php)

#### Example usage:
Synonyms:
```python
import poethu

poet = poethu.API(username="your_username", password="your_key")

synonyms = poet.get_szinonima(word="Helló", order="asc", max=5)

for i in range(len(synonyms)):
    synonym = synonyms[i]
    print(f"{i}: {synonym}")
```
Output:
```
0: üdv
1: szia
2: cső
3: szervusz
4: hahó
```
Poems:
```python
import poethu

poet = poethu.API(username="your_username", password="your_key")

poems = poet.get_versek(category="gyerekvers", max=2, order="desc", continue_from=20)
# The output is raw, so we need to format it.

# You only need to use loops when you want to get more poems than 1
# If you not, you can simply use title = poet.get_title(poems)

for i in range(len(poems)):
    title = poet.get_title(poems)[i]
    text = poet.get_text(poems)[i]
    poem = poet.get_text(poems)[i]
    author = poet.get_author(poems)[i]
    category = poet.get_category(poems)[i]
    favs = poet.get_favs(poems)[i]
    id = poet.get_id(poems)[i]
    url = poet.get_url(poems)[i]

    print(f"Title: {title}")
    print(f"Poem text: \n{text}")
    print(f"Author: {author}")
    print(f"Category: {category}")
    print(f"Favs: {favs}")
    print(f"ID: {id}")
    print(f"URL: {url}")
```
Output:
```
Title: Farkas és a bárány
Poem text:
Én vagyok a farkas,
Fél tőlem a szarvas,
Ha prédára akadok,
Az erdőben maradok.

Az én nevem barika,
Barátom a Gabika,
Jaj, de félve lépkedek,
Ha erdőbe tévedek.
Author: Tóth Marianna (banattanc)
Category: Gyerekvers
Favs: 23
ID: 351818
URL: https://www.poet.hu/vers/351818
```

