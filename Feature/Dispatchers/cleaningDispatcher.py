from loguru import logger
from DB.models.noSqlBaseDocument import NoSQLBaseDocument
from DB.models.vectorBaseDocument import VectorBaseDocument
from DB.types.types import DataCategory
from Feature.Handlers.CleaningDataHandler import (
    CleaningDataHandler,
    PostCleaningHandler,
    ArticleCleaningHandler,
    RepositoryCleaningHandler,
)

class CleaningHandlerFactory:
    @staticmethod
    def create_handler(data_category: DataCategory) -> CleaningDataHandler:
        if data_category == DataCategory.POSTS:
            return PostCleaningHandler()
        elif data_category == DataCategory.ARTICLES:
            return ArticleCleaningHandler()
        elif data_category == DataCategory.REPOSITORIES:
            return RepositoryCleaningHandler()
        else:
            raise ValueError("Unsupported data ")

class CleaningDispatcher:
    cleaning_factory = CleaningHandlerFactory()
    @classmethod
    def dispatch(cls, data_model: NoSQLBaseDocument) -> VectorBaseDocument:
        data_category = DataCategory(data_model.get_collection_name())
        handler = cls.cleaning_factory.create_handler(data_category)
        clean_model = handler.clean(data_model)
        logger.info(
        "Data cleaned successfully.",
        data_category=data_category,
        cleaned_content_len=len(clean_model.content),
        )
        return clean_model
