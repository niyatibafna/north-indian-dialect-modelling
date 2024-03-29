# Data Collection for the Indic Dialect Continuum (26 languages)

## Collected Data

Here is the summary of the collected data. We separate the languages into Bands 1, 2, and 3, by decreasing availability of pre-existing data, and report averages per band. Band 3 (i.e. Rajasthani, Himachali onwards) are currently zero-resourced.


| Language      | Folksongs | Poetry | Folksongs tokens | Poetry tokens      | Total Pieces | Total tokens |
|---------------|-----------|--------|------------------|--------------------|--------------|-------------------|
| Hindi-urdu    | 1         | 54408  | 100              | 7127897            | 54409        | 7127997           |
| Marathi       | 5         | 30     | 1412             | 1915               | 35           | 3327              |
| Nepali        | 0         | 4753   | 0                | 692657             | 4753         | 692657            |
| Sindhi        | 0         | 500    | 0                | 51458              | 500          | 51458             |
| Punjabi       | 754       | 0      | 69595            | 0                  | 754          | 69595             |
| Gujarati      | 14        | 624    | 1795             | 73363              | 638          | 75158             |
| Bangla        | 12        | 0      | 838              | 0                  | 12           | 838               |
| **Avg.**      |           |        |                  |                    |              | 1,145,861.43      |
| Magahi        | 340       | 376    | 37587            | 47167              | 716          | 84754             |
| Awadhi        | 47        | 1333   | 4942             | 495137             | 1380         | 500079            |
| Bhojpuri      | 131       | 1275   | 20350            | 177289             | 1406         | 197639            |
| Maithili      | 0         | 1552   | 0                | 218339             | 1552         | 218339            |
| Brajbhasha    | 83        | 1441   | 8883             | 151156             | 1524         | 160039            |
| **Avg.**        |           |        |                  |                    |              | 232170.00         |
| Rajasthani    | 67        | 1790   | 7404             | 180320             | 1857         | 187724            |
| Himachali     | 3         | 0      | 466              | 0                  | 3            | 466               |
| Koraku        | 177       | 0      | 15509            | 0                  | 177          | 15509             |
| Baiga         | 35        | 0      | 13848            | 0                  | 35           | 13848             |
| Nimaadi       | 157       | 0      | 14056            | 0                  | 157          | 14056             |
| Khadi\_boli   | 42        | 0      | 4507             | 0                  | 42           | 4507              |
| Garwali       | 128       | 449    | 33380            | 59288              | 577          | 92668             |
| Chattisgarhi  | 92        | 378    | 33504            | 49722              | 470          | 83226             |
| Bhil          | 155       | 0      | 27326            | 0                  | 155          | 27326             |
| Sanskrit      | 2         | 248    | 184              | 95450              | 250          | 95634             |
| Angika        | 96        | 6773   | 21419            | 1243727            | 6869         | 1265146           |
| Hariyanvi     | 554       | 930    | 49122            | 183881             | 1484         | 233003            |
| Kannauji      | 6         | 0      | 327              | 0                  | 6            | 327               |
| Bundeli       | 326       | 0      | 26928            | 0                  | 326          | 26928             |
| Malwi         | 129       | 0      | 9626             | 0                  | 129          | 9626              |
| Kumaoni       | 9         | 0      | 1028             | 0                  | 9            | 1028              |
| Bhadavari     | 8         | 0      | 990              | 0                  | 8            | 990               |
| Pali          | 0         | 27     | 0                | 5859               | 27           | 5859              |
| Bajjika       | 0         | 71     | 0                | 7414               | 71           | 7414              |
| **Avg.**      |           |        |                  |                    |              | 109,751.842       |

## Available Data

The folksongs listed for all the languages above are available ... TODO

## Running the crawler

Requirements:

* [```requests```](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiy-9nTveb4AhWau6QKHa0jBhYQFnoECAYQAQ&url=https%3A%2F%2Fpypi.org%2Fproject%2Frequests%2F&usg=AOvVaw1-RuMU-5ZQL9xNuNrQ3jg4)

* [```BeautifulSoup```](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjz2cPhveb4AhUQy6QKHbWqCQUQFnoECAYQAQ&url=https%3A%2F%2Fbeautiful-soup-4.readthedocs.io%2Fen%2Flatest%2F&usg=AOvVaw3ox0yL2znF6w6A1_ShHM5s)

To crawl the poetry or folksongs, simply run:

```python crawler_bfs_poetry.py```

or 

```python crawler_bfs_folksongs.py```

respectively. The data will be crawled into the directory ```../data/poetry/``` (similarity for folksongs). Intermediate bfs variables will be stored in ```crawl_variables/```; this can be changed if required or automatically deleted post-crawl.







