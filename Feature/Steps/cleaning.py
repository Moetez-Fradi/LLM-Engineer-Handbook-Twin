from typing import Annotated
from Feature.Dispatchers.cleaningDispatcher import CleaningDispatcher
from zenml import step
from zenml.steps import get_step_context
from DB.models.cleanedDocuments import CleanedDocument
from loguru import logger

@step
def clean_documents(documents: Annotated[list, "raw_documents"]) -> Annotated[list, "cleaned_documents"]:
    cleaned_documents = []
    for document in documents:
        cleaned_document = CleaningDispatcher.dispatch(document)
        cleaned_documents.append(cleaned_document)

    step_context = get_step_context()
    step_context.add_output_metadata(output_name="cleaned_documents",
    metadata=_get_metadata(cleaned_documents))
    return cleaned_documents

def _get_metadata(cleaned_documents: list[CleanedDocument]) -> dict:
    metadata = {"num_documents": len(cleaned_documents)}

    for document in cleaned_documents:
        category = document.get_category()

        if category not in metadata:
            metadata[category] = {"authors": [], "num_documents": 0}

        metadata[category]["num_documents"] += 1

        author = document.author_full_name
        if isinstance(author, list):
            author = " ".join(author)

        metadata[category]["authors"].append(author)

    for value in metadata.values():
        if isinstance(value, dict):
            value["authors"] = list(set(value["authors"]))

    return metadata
