import re
from langchain_text_splitters import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from Feature.Network.EmbeddingModelSingleton import EmbeddingModelSingleton

embedding_model = EmbeddingModelSingleton()

def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    character_splitter = RecursiveCharacterTextSplitter(separators=["\n\n"], chunk_size=chunk_size, chunk_overlap=0)
    text_split_by_characters = character_splitter.split_text(text)

    token_splitter = SentenceTransformersTokenTextSplitter(
        chunk_overlap=chunk_overlap,
        tokens_per_chunk=embedding_model.max_input_length,
        model_name=embedding_model.model_id,
    )
    chunks_by_tokens = []
    for section in text_split_by_characters:
        chunks_by_tokens.extend(token_splitter.split_text(section))

    return chunks_by_tokens

def chunk_article(text: str, min_length: int, max_length: int) -> list[str]:
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s", text)

    extracts = []
    current_chunk = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence + " "
        else:
            if len(current_chunk) >= min_length:
                extracts.append(current_chunk.strip())
            current_chunk = sentence + " "

    if len(current_chunk) >= min_length:
        extracts.append(current_chunk.strip())

    return extracts


def clean_text(text: str) -> str:
    text = re.sub(r"[^\w\s.,!?]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_user_name(full_name: str) -> tuple[str, str]:
    """Splits a full name into first and last name.

    Args:
        full_name (str): The full name of the user.
    Returns:
        tuple[str, str]: A tuple containing the first name and last name.
    """
    parts = full_name.strip().split()
    if len(parts) == 0:
        return "", ""
    elif len(parts) == 1:
        return parts[0], ""
    else:
        first_name = parts[0]
        last_name = " ".join(parts[1:])
        return first_name, last_name