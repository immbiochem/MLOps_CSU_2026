# Task4

## бот (PeiKibBreat2.py) с текстовой памятью + вилка по скилу пользователя: биологи/айтишники/обычные пользователи 

Скрипт с ассистентом PeiKibBreat2.py запускается следующей командой:

*python3 PeiKibBreat2.py*

При запуске необходимо указать идентификатор сессии, если ранее был диалог с ботом, либо задать новый id

Память находится в отдельной папке chat_histories: номера JSON файлов соответствуют идентификаторам сессии

## Пример диалога с записью в файл для *maple-preview-TQ1_0-head-Q4_K*:

___

(tool) a@1:~/МАГИСТРАТУРА/MLOps/code/box4$ python3 PeiKibBreat2.py
<sys>:0: LangChainDeprecationWarning: RunnableWithMessageHistory is deprecated. Use LangGraph's built-in persistence instead.
История сохраняется в папку 'chat_histories'.
Для выхода введите 'пока' 'выход', 'exit' или 'q'

Введите идентификатор
>1
Pei Kib Breat слушает...(Голос: 1)
> Привет, меня зовут Семён
/home/a/МАГИСТРАТУРА/MLOps/code/box4/PeiKibBreat2.py:107: LangChainDeprecationWarning: The class `ConversationBufferWindowMemory` was deprecated in LangChain 0.3.1 and will be removed in 2.0.0. Use `langchain.agents.create_agent` instead. For agents that need to remember prior interactions, use `create_agent` with checkpointing or the `Store` API. See https://docs.langchain.com/oss/python/langchain/short-term-memory and https://docs.langchain.com/oss/python/langchain/long-term-memory
  memory = ConversationBufferWindowMemory(
Pei Kib Breat: Ну, понял! Рад снова видеться. Чем могу помочь?

> Я занимаюсь биоинформатикой
Pei Kib Breat: Понял, ты занимаешься биоинформатикой. Что именно сейчас занимаешься? Может быть, построение моделей, анализ геномных данных, работа с большими наборами экспериментальных данных или что-то другое? Буду рад узнать подробнее.

> пока
Pei Kib Breat: Пока!
(tool) a@1:~/МАГИСТРАТУРА/MLOps/code/box4$ python3 PeiKibBreat2.py
<sys>:0: LangChainDeprecationWarning: RunnableWithMessageHistory is deprecated. Use LangGraph's built-in persistence instead.
История сохраняется в папку 'chat_histories'.
Для выхода введите 'пока' 'выход', 'exit' или 'q'

Введите идентификатор
>1
Pei Kib Breat слушает...(Голос: 1)
> Привет, помнишь, чем я занимаюсь?
/home/a/МАГИСТРАТУРА/MLOps/code/box4/PeiKibBreat2.py:107: LangChainDeprecationWarning: The class `ConversationBufferWindowMemory` was deprecated in LangChain 0.3.1 and will be removed in 2.0.0. Use `langchain.agents.create_agent` instead. For agents that need to remember prior interactions, use `create_agent` with checkpointing or the `Store` API. See https://docs.langchain.com/oss/python/langchain/short-term-memory and https://docs.langchain.com/oss/python/langchain/long-term-memory
  memory = ConversationBufferWindowMemory(
Pei Kib Breat: Да, помню! Ты Семён, биоинформатик. Чем могу помочь?

> Какие существуют генетические эволюционные особенности у растений?
Pei Kib Breat: Приветствую. Как учёный-биолог, я рассматриваю растения как ключевой группу живых организмов, в которых наблюдается один из самых ярких примеров генетических эволюционных механизмов. Ответ ассистента корректен в общих чертах, но я хочу дополнить его более глубоким, современным взглядом, выделив те аспекты, которые часто остаются в стороне при изучении растительной генетики.

### 1. Полиплоидия и плюралии как главные «генетические трансформаторы»
У растений полиплоидия (повторение хромосом) — это не просто хромосомная особенность, а мощный инструмент эволюции. Она позволяет мгновенно создать нового вид, так как отсутствует гибридизация (см. ниже). Например, триплоидия у злаков (пшеница, пшеница-перекрестная зелёная пшеница) и тетраплоидия у яблоней (домашняя вишня, малина) — это прямые следы генетического разрыва из-за полиплоидии. Плюралии (несколько подвижных хромосомных наборов) возникают через гибридию с разными пloidностями и дают гибридные особенности (нормализм, гибрид-фитотипия), что в растениях встречается гораздо чаще, чем в животных.

### 2. Гибридизация и биологические викинги — главные двигатели растительной эволюции
В отличие от животного мира, где гибридизация часто приводит к гибридной инвалидности, у растений гибридизация — нормальная часть жизненной истории. Многие виды (например, тропические папоротники, орхидеи) возникли именно из гибридов. Особую роль играют «гетероспоры» и гетероспориальные ферменты: гетероспорообразные растения (например, бресяния) часто имеют гибридные геномы, а гетероспория может быть аполиплоидной или динаполиплоидной, что генерирует новые аллоаллоидные гены. Эпигенетические изменения, связанные с гетероспорацией, также способствуют быстрому адаптационному разрыву.

### 3. Отсутствие генетического разрыва и панмиксия
Растения (как и некоторые животные, например, медведи) имеют гибкую структуру популяций: отсутствие чёткого генетического разрыва между подгруппами (пан

> пока
Pei Kib Breat: Пока!
(tool) a@1:~/МАГИСТРАТУРА/MLOps/code/box4$ python3 PeiKibBreat2.py
<sys>:0: LangChainDeprecationWarning: RunnableWithMessageHistory is deprecated. Use LangGraph's built-in persistence instead.
История сохраняется в папку 'chat_histories'.
Для выхода введите 'пока' 'выход', 'exit' или 'q'

Введите идентификатор
>2
Pei Kib Breat слушает...(Голос: 2)
> Привет, я Саймон, датасаентист
/home/a/МАГИСТРАТУРА/MLOps/code/box4/PeiKibBreat2.py:107: LangChainDeprecationWarning: The class `ConversationBufferWindowMemory` was deprecated in LangChain 0.3.1 and will be removed in 2.0.0. Use `langchain.agents.create_agent` instead. For agents that need to remember prior interactions, use `create_agent` with checkpointing or the `Store` API. See https://docs.langchain.com/oss/python/langchain/short-term-memory and https://docs.langchain.com/oss/python/langchain/long-term-memory
  memory = ConversationBufferWindowMemory(
Pei Kib Breat: Понял, Саймон. Рад познакомиться! Обычно я всегда отвечаю на вопросы и помогаю в чем угодно. Давай продолжим разговор — что тебя интересует в дата-аналитике?

> Как провести корреляционный анализ данных на python?
Pei Kib Breat: Для корреляционного анализа данных в Python наиболее часто применяются библиотеки `pandas`, `scipy` и `seaborn`. Выбор метода (линейная, монотонная или ранговая) зависит от типа данных и задачи.

### 1. Базовый подход с `pandas` и `scipy`
```python
import pandas as pd
from scipy.stats import pearsonr, spearmanr, kendalltau

# df - DataFrame с нужными столбцами
# Линейная корреляция (Пирсон)
corr_pearson, p_value_pearson = pearsonr(df['column1'], df['column2'])
# Монотонная корреляция (Спирмен)
corr_spearman, p_value_spearman = spearmanr(df['column1'], df['column2'])
# Ранговая корреляция (Кендал)
corr_kendall, p_value_kendall = kendalltau(df['column1'], df['column2'])
```

### 2. Визуализация
```python
import seaborn as sns
import matplotlib.pyplot as plt

# Тепловая карта матрицы корреляций
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.show()
```

### 3. Если нужно сразу визуализировать корреляции
```python
sns.pairplot(df, vars=['col1', 'col2'], kind='scatter')
sns.pairplot(df, vars=['col1', 'col2'], kind='kde')
```

### 4. Автоматизация с `pandas`
```python
corr_matrix = df.corr(method='pearson')  # или 'spearman'/'kendall'
```

### Важные замечания
- `pearsonr` требует отсутствие пропусков и линейной зависимости. Если зависимость монотонная, лучше использовать `spearmanr`.
- Для выборки корреляционный коэффициент (R) — это мера силы и направления связей. `p_value` показывает степень значимости (если < 0.05 — значимо).
- `scipy.stats` работает с одномерными массивами (Series), но можно передавать списки или массивы numpy.

### Пример полного цикла
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка данных
df = pd.read_csv('data.csv')

# Корреляционная матрица
corr_matrix = df.corr(method='pearson')

# Тепловая карта
sns.heatmap(corr_matrix, annot=True, cmap='RdBu', vmin=-1, vmax=1)
plt.title('Корреляционная матрица (Пирсон)')
plt.show()

# Рассмотрим только одну пару
x = df['x_column']
y = df['y_column']
corr, p = pearsonr(x, y)
print(f'Pearson R: {corr:.3f}, p-value: {p:.4f}')
```

Этот подход покрывает большинство задач корреляционного анализа в Python. Для более сложных (например, временные ряды) можно использовать `statsmodels` или `pandas.plotting.scatter_matrix`.

> пока
Pei Kib Breat: Пока!
(tool) a@1:~/МАГИСТРАТУРА/MLOps/code/box4$ python3 PeiKibBreat2.py
<sys>:0: LangChainDeprecationWarning: RunnableWithMessageHistory is deprecated. Use LangGraph's built-in persistence instead.
История сохраняется в папку 'chat_histories'.
Для выхода введите 'пока' 'выход', 'exit' или 'q'

Введите идентификатор
>2
Pei Kib Breat слушает...(Голос: 2)
> Привет, что я спрашивал последний раз?                                        
/home/a/МАГИСТРАТУРА/MLOps/code/box4/PeiKibBreat2.py:107: LangChainDeprecationWarning: The class `ConversationBufferWindowMemory` was deprecated in LangChain 0.3.1 and will be removed in 2.0.0. Use `langchain.agents.create_agent` instead. For agents that need to remember prior interactions, use `create_agent` with checkpointing or the `Store` API. See https://docs.langchain.com/oss/python/langchain/short-term-memory and https://docs.langchain.com/oss/python/langchain/long-term-memory
  memory = ConversationBufferWindowMemory(
Pei Kib Breat: Понял. Вы спрашивали про корреляционный анализ данных на Python. Если нужно уточнить или перейти к другому вопросу — дайте знать.

> пока
Pei Kib Breat: Пока!
