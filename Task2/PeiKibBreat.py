from pathlib import Path
from typing import Any
from langchain_core.runnables import Runnable


class FileMemory(Runnable):
    """Читает текст из файла и возвращает его как строку.

    Если файла нет — возвращает пустую строку (не падаем).
    Если файл пустой — тоже пустую строку.
    """

    def __init__(self, path: str = "mem.txt"):
        self.path = Path(path)

    def invoke(self, input: Any = None, config=None, **kwargs) -> str:
        if not self.path.exists():
            return ""
        text = self.path.read_text(encoding="utf-8").strip()
        return text

    #
    async def ainvoke(self, input: Any = None, config=None, **kwargs) -> str:
        return self.invoke(input)

    def stream(self, input: Any = None, config=None, **kwargs):
        yield self.invoke(input)

    #
    def append(self, text: str) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(text.rstrip() + "\n")

    def clear(self) -> None:
        self.path.write_text("", encoding="utf-8")

###########################

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

llm = ChatOpenAI(
    model="maple",
    base_url="http://localhost:8080/v1", 
    api_key="not-needed",
    temperature=0.6,
)

memory = FileMemory("mem.txt")

def save_if_needed(answer: str) -> str:
    for line in answer.splitlines():
        if "ЗАПОМНИ:" in line.strip().upper():
            memory.append(line.split("ЗАПОМНИ:", 1)[1].strip())
    return answer

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Ты — ассистент с памятью.\n"
     "Текущая память:\n{memory}\n\n"
     "Если пользователь сообщает что-то важное о себе — "
     "в конце ответа добавь строку 'ЗАПОМНИ: <факт>'. Но только если этого факта ты не знаешь."),
    ("human", "{question}"),
])

chain = (
    {
        "memory": memory,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
    | RunnableLambda(save_if_needed)
)

###########################

def main():
    print("Pei Kib Breat слушает...")
    print("Напишите 'пока' чтобы покинуть чат.\n")
    while True:
        print('\n' + '*'*6 + "~ ^..^ ~ " + '*'*6)
        user_input = input(">: ").strip()
        if user_input.lower() == "пока":
            print("Пока!")
            break
        print("Pei Kib Breat: ", end="", flush=True)
        response = chain.invoke(user_input)
        print(response)

if __name__ == "__main__":
    main()
