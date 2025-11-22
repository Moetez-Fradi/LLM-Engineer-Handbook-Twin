from zenml import get_step_context, step
from typing import Annotated
from Logging.logger import logger
from utils.strings import split_user_name
from DB.models.documents import UserDocument
from DB.queries.fetch_all import fetch_all_data
from utils.getMetadata import _get_metadata

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