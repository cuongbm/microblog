from elasticsearch import NotFoundError
from flask import current_app


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return

    if not current_app.elasticsearch.indices.exists(index=index):
        create_index(index)
    payload={}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)

    current_app.elasticsearch.index(index=index, doc_type=index, id=model.id,
                                    body=payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)


def delete_index(index):
        current_app.elasticsearch.indices.delete(index=index, ignore=[400, 404])


def create_index(index):
    current_app.elasticsearch.indices.create(index=index, ignore=[400, 404])


def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index, doc_type=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']