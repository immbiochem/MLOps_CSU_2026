import json
import os
from typing import List
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_core.messages import BaseMessage, messages_from_dict, messages_to_dict
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnablePassthrough,
)
from langchain_openai import ChatOpenAI

# =====================================================================

class JSONChatMessageHistory(BaseChatMessageHistory):
    """Кастомный класс истории сообщений, сохраняющий данные в JSON файл."""
    
    def __init__(self, session_id: str, file_directory: str = "chat_histories"):
        self.session_id = session_id
        self.file_directory = file_directory
        # Создаем папку для историй, если её нет
        os.makedirs(self.file_directory, exist_ok=True)
        self.file_path = os.path.join(self.file_directory, f"{session_id}.json")

    @property
    def messages(self) -> List[BaseMessage]:
        """Загружает сообщения из JSON-файла при каждом обращении."""
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Восстанавливаем объекты сообщений LangChain из словаря
                return messages_from_dict(data)
        except (json.JSONDecodeError, KeyError):
            return []

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Добавляет новые сообщения в JSON-файл."""
        # 1. Читаем текущую историю
        current_messages = self.messages
        # 2. Добавляем новые сообщения
        current_messages.extend(messages)
        # 3. Сериализуем объекты сообщений в стандартный формат словарей LangChain
        serializable_data = messages_to_dict(current_messages)
        # 4. Перезаписываем файл
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(serializable_data, f, ensure_ascii=False, indent=2)

    def clear(self) -> None:
        """Очищает историю (удаляет файл)."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

# =====================================================================

def dummy_bio_classifier(inputs: dict) -> str:
    """Простой классификатор принадлежности текста;
       определяет, принадлежит ли вопрос к области биологии, информатики или нейтрален;
    """
    text = inputs.get("text", "").get("text", "").lower()
    #
    biological_buff = ['био','молекул','меди','тоз','клин','клетк','клеточ','эволю','нукл','митохон','ген','хромо','раст']
    computer_science_buff = ['инфор','модел','пайпл','алгоритм','сети','python','c+','код','данны','мид','джун','тимлид','созвон']
    #
    bio_score = 0
    cs_score = 0
    #
    for bio in biological_buff:
        if bio in text.lower():
            bio_score+=1
    #
    for cs in computer_science_buff:
        if cs in text.lower():
            cs_score+=1
    #
    if (bio_score - cs_score) > 1:
        return 'bio'
    elif (bio_score - cs_score) < -1:
        return 'cs'
    else:
        return 'norm'


# =====================================================================

llm = ChatOpenAI(
    model="maple",
    base_url="http://localhost:8080/v1", 
    api_key="not-needed",
    temperature=0.6,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты ИИ-ассистент. Отвечай лаконично."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{user_input}")
])

base_chain = prompt | llm | StrOutputParser()

def get_session_history(session_id: str):
    memory = ConversationBufferWindowMemory(
        chat_memory=JSONChatMessageHistory(session_id=session_id),
        k=3,
        return_messages=True,
    )
    return memory.chat_memory


# =====================================================================

classifier_runnable = RunnableLambda(dummy_bio_classifier)

bio_prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты — ассистент-биолог."),
    ("human",
     "Был задан вопрос на биологическую тему"
     "Ответь как ученый-биолог\n\n"
     "Исходный вопрос: {user_input}\n"
     "Ответ ассистента: {answer}"),
])

cs_prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты — ассистент-информатик."),
    ("human",
     "Был задан вопрос на компьютерную тему"
     "отвечай как технический специалист\n\n"
     "Исходный вопрос: {user_input}\n"
     "Ответ ассистента: {answer}"),
])

neutral_prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты — ассистент."),
    ("human",
     "Ответ был нейтральным. Общайся как обычно. Отвечай на вопросы.\n\n"
     "Исходный вопрос: {user_input}\n"
     "Ответ ассистента: {answer}"),
])

router = RunnableBranch(
        (
            lambda x: x["category"] == "bio",
            bio_prompt | llm | StrOutputParser(),
        ),
        (
            lambda x: x["category"] == "cs",
            cs_prompt | llm | StrOutputParser(),
        ), 
        neutral_prompt | llm | StrOutputParser()
        )

branch_chain = RunnablePassthrough.assign(answer=base_chain) | RunnablePassthrough.assign(text=(RunnableLambda(lambda x: {"text": x["answer"]}))) | RunnablePassthrough.assign(category=classifier_runnable) | router


# Оборачиваем цепочку для автоматической работы с нашей JSON-памятью
bot_chain = RunnableWithMessageHistory(
    branch_chain,
    get_session_history=get_session_history,
    input_messages_key="user_input",
    history_messages_key="chat_history"
)


# =====================================================================

print("История сохраняется в папку 'chat_histories'.")
print("Для выхода введите 'пока' 'выход', 'exit' или 'q'\n")

SESSION_ID = input("Введите идентификатор\n>").strip()

config = {"configurable": {"session_id": SESSION_ID}}

print(f"Pei Kib Breat слушает...(Голос: {SESSION_ID})")

while True:
    try:
        user_message = input("> ").strip()
        
        if user_message.lower() in ['пока', 'выход', 'exit', 'q']:
            print("Pei Kib Breat: Пока!")
            break
            
        if not user_message:
            continue
            
        # Отправка сообщения
        response = bot_chain.invoke(
            {"user_input": user_message}, 
            config=config
        )
        text_content = response if isinstance(response, str) else getattr(response, "text", str(response))
        print(f"Pei Kib Breat: {text_content}\n")
        
    except KeyboardInterrupt:
        print("\nPei Kib Breat: Сессия завершена. Пока!")
        break
        