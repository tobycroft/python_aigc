import os

from flask import Blueprint
from langchain_community.vectorstores.milvus import Milvus

import tuuz.Database
import tuuz.Input
import tuuz.Ret
from app.v1.langchain.action.EmbeddingAction import EmbeddingAction

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('/text')
async def text():
    embeddings = EmbeddingAction().FromText(
        "过去一周，汽车圈所有的话题焦点基本就集中在小米SU7和雷军本人身上了。别管是不是有人刻意在炒热度，论全行业里都找不出任何一个可与之匹敌的对手。有人说，这是雷军自创建小米起就树立的人设，让太多不关注汽车的人来了兴趣，又有人说，这一切是SU7过人的产品力使得小米在细分市场难逢敌手。当然，按市场反响来看，雷军造车这件事还是取得了阶段性的成功。对此，不仅是当时坐在小米SU7上市发布会台下的何小鹏、李斌、李想等人已经感到压力了，车市随着而来地降价潮显然也是冲着小米去的。不过，相比一众在努力组织应对政策的车企，很搞笑的是，远在大洋彼岸的贾跃亭，阴阳怪气起来着实有一手。"
        ).Embedding()
    print(embeddings.GetDoc())
    # MILVUS_HOST = "10.0.0.174"
    # MILVUS_PORT = "19530"
    # vector_store = Milvus(embeddings.GetEmbedding(),
    #                       collection_name="collection_1",
    #                       connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT})
    #
    # vector_store.from_texts(embeddings.GetDoc(), embeddings.GetEmbedding(), collection_name="collection_1", connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT})
    # vector_store = Milvus.from_documents(
    #     embeddings.GetDoc(),
    #     embedding=embeddings.GetEmbedding(),
    #     collection_name="collection_1",
    #     connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT}
    # )
    #
    #
    # query1 = "托马斯是时间行者"
    # docs1 = vector_store.similarity_search_with_score(query1)
    # query2 = "Bilibili"
    # docs2 = vector_store.similarity_search_with_score(query2)

    # opt = vector_store.similarity_search_by_vector(embeddings.GetEmbedQuery("托马斯是时间行者"), top_k=3)
    # print(docs)
    return tuuz.Ret.success(0, "", embeddings.GetDoc())
