import os

from flask import Blueprint
from langchain_community.vectorstores.milvus import Milvus

import tuuz.Database
import tuuz.Input
import tuuz.Ret
from app.v1.langchain.action.EmbeddingAction import EmbeddingAction
from tuuz.input.post import Post

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('/text')
async def text():
    text = Post.Str("text")
    embeddings = EmbeddingAction().FromText(text).Embedding()
    print(embeddings.GetDoc())
    # embeddings = EmbeddingAction().Embedding()

    MILVUS_HOST = "10.0.0.174"
    MILVUS_PORT = "19530"

    vector_store = Milvus(embeddings.GetEmbedding(),
                          collection_name="collection_4",
                          connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT})
    vector_store.from_documents(embeddings.GetDoc(), embeddings.GetEmbedding(), collection_name="collection_4", connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT})
    # vector_store = Milvus.from_documents(
    #     embeddings.GetDoc(),
    #     embedding=embeddings.GetEmbedding(),
    #     collection_name="collection_3",
    #     connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT}
    # )

    #
    # query1 = "托马斯是时间行者"
    # docs1 = vector_store.similarity_search_with_score(query1)
    # query2 = "Bilibili"
    # docs2 = vector_store.similarity_search_with_score(query2)

    opt = vector_store.similarity_search_by_vector(embeddings.GetEmbedQuery(text), top_k=3)
    # print(docs)
    return tuuz.Ret.success(0, opt, embeddings.GetDoc())
