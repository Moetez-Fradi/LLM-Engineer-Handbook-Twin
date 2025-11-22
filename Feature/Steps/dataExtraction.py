from zenml import get_step_context, step
from typing import Annotated
from loguru import logger
from utils.strings import split_user_name
from DB.models.documents import UserDocument, Document
from DB.queries.fetch_all import fetch_all_data

@step
def query_data_warehouse(author_full_names: list[str],) -> Annotated[list, "raw_documents"]:
    documents = []
    authors = []
    for author_full_name in author_full_names:
        logger.info(f"Querying data warehouse for user: {author_full_name}")

        first_name, last_name = split_user_name(author_full_name)

        logger.info(f"First name: {first_name}, Last name: {last_name}")

        user = UserDocument.get_or_create(first_name=first_name, last_name=last_name)
        authors.append(user)

        results = fetch_all_data(user)
        user_documents = [doc for query_result in results.values() for doc in query_result]

        documents.extend(user_documents)

    step_context = get_step_context()
    step_context.add_output_metadata(output_name="raw_documents", metadata=_get_metadata(documents))
    
    return documents

def _get_metadata(documents: list[Document]) -> dict:
    metadata = {
        "num_documents": len(documents),
    }
    for document in documents:
        collection = document.get_collection_name()
        if collection not in metadata:
            metadata[collection] = {}
        if "authors" not in metadata[collection]:
            metadata[collection]["authors"] = list()

        metadata[collection]["num_documents"] = metadata[collection].get("num_documents", 0) + 1
        metadata[collection]["authors"].append(document.author_full_name)

    for value in metadata.values():
        if isinstance(value, dict) and "authors" in value:
            value["authors"] = list(set(value["authors"]))

    return metadata
