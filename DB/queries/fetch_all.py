from typing import Dict
from DB.models.documents import RepositoryDocument, PostDocument, ArticleDocument, Document, UserDocument
from DB.models.noSqlBaseDocument import NoSQLBaseDocument
from concurrent.futures import ThreadPoolExecutor
from loguru import logger

def fetch_all_data(user: UserDocument) -> Dict[str, list[Document]]:
    author_id = str(user.id)
    return {
        "repositories": RepositoryDocument.bulk_find(author_id=author_id),
        "posts": PostDocument.bulk_find(author_id=author_id),
        "articles": ArticleDocument.bulk_find(author_id=author_id),
    }