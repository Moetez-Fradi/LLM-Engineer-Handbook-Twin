def _get_metadata(documents: list) -> dict:
    return {
        "num_documents": len(documents),
        "authors": list({str(doc.author_id) for doc in documents if hasattr(doc, "author_id")}),
    }