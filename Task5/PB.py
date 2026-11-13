import chromadb
from sentence_transformers import SentenceTransformer

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI


# ---------- 1. Векторная база (как в первом скрипте) ----------
model = SentenceTransformer('../models/esm2_8M')
collection = chromadb.PersistentClient(path="../antibody_chroma_db").get_or_create_collection(
    name="antibody_protein_sequences", metadata={"hnsw:space": "cosine"},
)


# ---------- 2. Шаг «достать контекст» — твой голый код из первого скрипта ----------
def retrieve(question:str) -> str:
    question = question.split('*')[-1].split('?')[0]
    emb = model.encode([question]).tolist()
    res = collection.query(query_embeddings=emb, n_results=2, include=["documents","metadatas"])
    docs = res["documents"][0] if res["documents"] else []
    if not docs:
        return "В базе знаний нет подходящих записей."
    #
    meta = res["metadatas"][0] if res["metadatas"] else []
    context = "\n".join(f"Найдено антитело: {d[0]}; группа: {d[-1]['group']}" for d in zip(docs, meta))
    print()
    print(context)
    print()
    return context


# ---------- 3. LLM — обычный Runnable, ставится в цепочку как есть ----------
llm = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",
    model="maple",
    temperature=0.45,
)

# ---------- 4. Промпт — это и есть «сформировать сообщение с контекстом» ----------
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Отвечай СТРОГО по контексту."
     "В контексте указаны похожие антитела и группы патологий"
     "дай ответ в соответствии с контекстом"),
    ("human", "Контекст:\n{context}\n\nВопрос:\n{question}"),
])

# ---------- 5. Цепочка ----------
chain = (
    {"context": RunnableLambda(retrieve), "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# =====================================================================

print("> Биоинформатический RAG-инструмент для поиска последовательностей антител в кастомной базе данных\n")
print("> Для получения данных о совпадениях введите интересуемую последовательность, начиная с символа *\n")
print("> Для выхода введите 'пока' 'выход', 'exit' или 'q'\n")


while True:
    try:
        user_message = input("> ").strip()
        
        if user_message.lower() in ['пока', 'выход', 'exit', 'q']:
            print("PKB: Пока!")
            break
            
        if not user_message:
            continue

        #
        text_content = chain.invoke(user_message)
        print(f"PKB: {text_content}\n")
        
    except KeyboardInterrupt:
        print("\nPKB: Сессия завершена. Пока!")
        break
