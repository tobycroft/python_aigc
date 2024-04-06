import os

from flask import Blueprint
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.embeddings.huggingface import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores.milvus import Milvus
from langchain_text_splitters import CharacterTextSplitter

import tuuz.Database
import tuuz.Input
import tuuz.Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('/text')
async def text():
    loader = WebBaseLoader("https://www.baidu.com")
    # print(loader)
    # loader = TextLoader("story.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    model_name = "./extend/bge-large-zh-v1.5/"
    model_kwargs = {'device': 'cuda'}
    encode_kwargs = {'normalize_embeddings': True}  # set True to compute cosine similarity
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
        query_instruction=""
    )

    MILVUS_HOST = "10.0.0.174"
    MILVUS_PORT = "19530"

    vector_store = Milvus.from_documents(
        docs,
        embedding=embeddings,
        collection_name="collection_1",
        connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT}
    )

    query = "托马斯是时间行者"
    docs = vector_store.similarity_search_with_score(query)

    print(docs)
    return tuuz.Ret.success(0, )
