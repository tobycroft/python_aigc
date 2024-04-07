from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.embeddings.huggingface import HuggingFaceBgeEmbeddings
from langchain_text_splitters import CharacterTextSplitter


class EmbeddingAction:
    __doc = []
    __embedding: HuggingFaceBgeEmbeddings = None

    def __init__(self):
        pass

    def FromWeb(self, url, chunk_size=100, chunk_overlap=0):
        loader = WebBaseLoader(url)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_documents(documents)
        self.__doc = docs
        return self

    def FromText(self, text, chunk_size=100, chunk_overlap=0):
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_documents(text)
        self.__doc = docs
        return self

    def Embedding(self):
        model_name = "BAAI/bge-large-zh-v1.5"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': True}  # set True to compute cosine similarity
        self.__embedding = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            cache_folder="./huggingface/bge-large-zh-v1.5",
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
            query_instruction="",
        )
        return self

    def GetEmbedding(self):
        return self.__embedding

    def GetEmbedQuery(self, query):
        return self.__embedding.embed_query(query)

    def GetDoc(self):
        return self.__doc
