from sentence_transformers import SentenceTransformer
import re
Template = "{title},  {}"


def search_by_embeddings(data, query, by="", accuracy=0.4, template="", model='sentence-transformers/all-MiniLM-L6-v2'):
    if not data:
        raise Exception('The "data" prop is required!')
    if not query:
        raise Exception('The "query" prop is required!')
    if not by and not template:
        raise Exception(
            'At least one of the props "by" or "template" is needed!')
    elif by and template:
        prop_names = re.findall(r'\{(.*?)\}', template)
        data_formatted = [template.format(
            **{prop: item[prop] for prop in prop_names}) for item in data]
        print(data_formatted)

    elif template:
        prop_names = re.findall(r'\{(.*?)\}', template)
        data_formatted = [template.format(
            **{prop: item[prop] for prop in prop_names}) for item in data]

    else:
        data_formatted = [item[by] for item in data]

    model_ = SentenceTransformer(model)
    embeddings = model_.encode(data_formatted)
    embedings_list = embeddings.tolist()

    def dotProduct(a, b):
        if len(a) != len(b):
            raise Exception('Both embeddings must have the same length!')

        result = 0

        for i, item in enumerate(a):
            result += a[i] * b[i]

        return result
    q_embedding = model_.encode(query).tolist()

    similarities_order = []
    for embedding in embedings_list:
        similarity = dotProduct(embedding, q_embedding)
        similarities_order.append(similarity)

    sorted_indices = sorted(range(len(similarities_order)),
                            key=lambda k: similarities_order[k], reverse=True)

    results = []
    for index in sorted_indices:
        similar = similarities_order[index]
        if similar <= accuracy:
            continue
        else:
            # Agregar los datos que cumplan el umbral
            results.append(data[index])

    return results
