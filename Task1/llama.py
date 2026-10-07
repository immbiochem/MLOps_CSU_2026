
import datetime
from openai import OpenAI
import argparse

def get_aminoacids(*args):
    codon_table = '''
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*', 'TGA':'*' # * — Стоп-кодоны
        '''
    return codon_table


def get_time(*args):
    now = datetime.datetime.now().strftime("%H:%M")
    return f"Текущее время: {now}."


AVAILABLE_FUNCTIONS = {
    "время": get_time,
    "кодоны": get_aminoacids
    }



SYSTEM_PROMPT = """Вы — полезный ИИ-ассистент. У вас есть доступ к встроенным функциям. 
Если пользователю нужна информация, которой у вас нет (актуальное время, таблица кодонов), вы ОБЯЗАНЫ вызвать функцию прямо в тексте своего ответа, используя специальный формат.

Формат вызова: [CALL: имя_функции(аргумент)]

Доступные функции:
- [CALL: время()] — узнать текущее время (без аргументов).
- [CALL: кодоны()] — напечатать таблицу кодонов (без аргументов).

Пример: Если спросили про время, напишите: "Секунду, я проверю. [CALL: время]"
Ничего не придумывайте сами, если требуется вызов функции!"""

client = OpenAI(
  base_url="http://localhost:8080/v1",
  api_key="not-needed"
)

import re

CALL_PATTERN = r"\[CALL:\s*(\w+)\((.*?)\)\]"

def run_agent_loop(user_message, openai_client, model):
    # 
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]
    model_ = "llama-3.2-3b-instruct" if model == 'lama' else "qwen2.5-3b"
    # 
    for _ in range(3):
        response = client.chat.completions.create(
                    model=model_,  # Имя модели может быть любым
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
        #
        assistant_text = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_text})
        
        # 
        match = re.search(CALL_PATTERN, assistant_text)
        
        if match:
            func_name = match.group(1)
            func_arg = match.group(2).strip().strip("'\"") # убираем лишние кавычки
            
            # 
            if func_name in AVAILABLE_FUNCTIONS:
                try:
                    function_result = AVAILABLE_FUNCTIONS[func_name](func_arg)
                except Exception as e:
                    function_result = f"Ошибка при выполнении функции: {str(e)}"
            else:
                function_result = f"Ошибка: Функция {func_name} не существует."
                
            # 
            messages.append({
                "role": "user", 
                "content": f"[ОТВЕТ ФУНКЦИИ {func_name}]: {function_result}"
            })
            
            # 
            continue
        else:
            # 
            return assistant_text

    return "Превышено количество итераций агента."

def main(model, log):
    print("--- Консольный REPL-чат на Python ---")
    print("Введите 'выход' или 'пока', чтобы завершить общение.\n")
    buffer = []
    # Loop
    while True:
        try:
            # Read
            user_input = input("Вы: ")
            buffer.append("Вы: "+user_input)

            if user_input.lower() == "пока" or user_input.lower() == "выход":
                break
            
            if not user_input.strip():
                continue
            # 
            response = run_agent_loop(user_input, client, model)
            buffer.append("Бот: "+response)
            #
            print(f"Бот: {response}\n")
                            
        except (KeyboardInterrupt, EOFError):
            print("\nЧат принудительно завершен.")
            break
    #
    with open(log, "a", encoding="utf-8") as file:
        stamp = datetime.datetime.now().strftime("%H:%M")
        file.write(f'\n_ _ _ _ _ _ _ _ _ _ START OF SESSION [{stamp}]_ _ _ _ _ _ _ _ _ _ _ _ _\n')
        for line in buffer:
            file.write(line+'\n')
        #
        file.write('_ _ _ _ _ _ _ _ _ _ END OF SESSION _ _ _ _ _ _ _ _ _ _ _ _ _\n\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="type of LLM", type=str)
    parser.add_argument("--log", help="name of log.txt", type=str)
    args = parser.parse_args()
    #
    MODEL = args.model
    LOG = args.log
    #
    main(MODEL, LOG)
