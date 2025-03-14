from src.utils.embedding_model import EmbeddingModel
from src.utils.db_model import DBModel
from src.utils.llm_model import LLMModel


class RAG:
    def __init__(self, embedding_model: EmbeddingModel, vector_db: DBModel, llm: LLMModel):
        """
        Initialize a RAG pipeline with the given models.
        :param embedding_model: Embedding model to generate embeddings for the query.
        :param vector_db: Vector database to retrieve context for the query.
        :param llm: Language model to generate responses for the query.
        """
        self.embedding_model = embedding_model
        self.vector_db = vector_db
        self.llm = llm

    def run(self, query: str, top_k: int = 1) -> tuple[str, list]:
        """
        Run the RAG pipeline with the given query and return the response.
        :param query: Query from the user.
        :param top_k: Number of documents to retrieve from the database.
        :return:
            response: Response generated by the LLM.
            results: List of all metadata retrieved from the database.
        """
        # 1. Generate embedding for the query
        query_embedding = self.embedding_model.generate_embeddings(query)

        # 2. Query the database to retrieve context
        context, results = self.vector_db.query_db(query_embedding, top_k)
        llm_context = " ".join(context)

        # 3. Formulate the full prompt for the LLM
        prompt = f"Context: {llm_context}\n\nQuestion: {query}\nAnswer:"

        # 4. Generate and return the response
        return self.llm.generate_response(prompt), results
