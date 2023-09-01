# QUESE

"Quese" allows you implement in an easy way a Search Algoritm, based on Embeddings and Similarity Search, in your Python apps.

## INSTALLATION

You can install "quese" with pip:

```bash
pip install quese
```
## FAST GUIDE
```
results = search_by_embeddings(data, "Here you query!", "title")
```
### Params

#### data:
It's the first param, it's **REQUIRED**, and it must be a **list of dictionaries**.

#### query:
It's the second param, it's **REQUIRED** as well, and it represent the query you want to pass.
Type: **string**

#### by:
It's the third param, it's **only REQUIRED if you don't pass a template**, and it represent the value of your dictionaries that you are searching for.
For example, if you want to search in  a list of products, your "by" param could be the prop "name" of each product.
Type: **string**
