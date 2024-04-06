import os

from flask import Blueprint

import tuuz.Database
import tuuz.Input
import tuuz.Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)

from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Milvus


@Controller.post('/')
def slash():
    return Controller.name


@Controller.before_request
def before():
    token = tuuz.Input.Header.String("token")
    data = tuuz.Database.Db().table("ai_project").where('token', token).find()
    if data is None:
        return tuuz.Ret.fail(400, 'project未启用')
    pass


@Controller.post('/text')
async def text():
    loader = WebBaseLoader("https://www.baidu.com")
    # loader = TextLoader("story.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    model_name = "/extend/bge/"
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
