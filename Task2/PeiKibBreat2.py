import json
import os
from typing import List
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, messages_from_dict, messages_to_dict
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
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

base_chain = prompt | llm

def get_json_history(session_id: str) -> JSONChatMessageHistory:
    """Функция-фабрика для RunnableWithMessageHistory."""
    return JSONChatMessageHistory(session_id=session_id)

# Оборачиваем цепочку для автоматической работы с нашей JSON-памятью
bot_chain = RunnableWithMessageHistory(
    base_chain,
    get_session_history=get_json_history,
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
        
        print(f"Pei Kib Breat: {response.content}\n")
        
    except KeyboardInterrupt:
        print("\nPei Kib Breat: Сессия завершена. Пока!")
        break