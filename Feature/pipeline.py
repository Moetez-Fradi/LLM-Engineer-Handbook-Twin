from zenml import pipeline
from Steps.dataExtraction import query_data_warehouse
from Steps.cleaning import clean_documents
from Steps.chunkingEmbedding import chunk_and_embed
from Steps.loading import load_to_vector_db

@pipeline
def feature_engineering(author_full_names: list[str]) -> None:
    raw_documents = query_data_warehouse(author_full_names)

    cleaned_documents = clean_documents(raw_documents)

    last_step_1 = load_to_vector_db(cleaned_documents)

    embedded_documents = chunk_and_embed(cleaned_documents)

    last_step_2 = load_to_vector_db(embedded_documents)
    
    return [last_step_1.invocation_id, last_step_2.invocation_id]