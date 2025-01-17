#Загрузка библиотек
from tkinter import *
from tkinter import filedialog
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import pymorphy2

# Инициализация стоп-слов для русского языка и анализатора, который используется для лемматизации от pymorphy2
nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))
morph = pymorphy2.MorphAnalyzer()

#функция, в которой загружается пользовательский файл. Используем для этого модуль filedialog и функцию askopenfilename
def open_file():
    file_path = filedialog.askopenfilename(title = "Выберите текстовый файл", filetypes = [("Text files", ".txt")])
    if file_path != "": # проверяем, что файл был выбран пользователем, то есть путь не нулевой
        with open(file_path, "r", encoding = "UTF-8") as file:
            text = file.read() # считываем файл
            text_widget.delete(1.0, END) #очищаем виджет с текстом, если там до этого был текст
            text_widget.insert(END, text) # и вставляем текст в виджет, чтобы тот отображался на экране
            return text
    else:
        return None

# Функция, подсчитывающая количество слов в тексте и среднее время его прочтения
def num_of_words(text):
    words = text.split() # делим текст на слова
    number_of_words = len(words) # считаем количество слов
    avg_reading_time = number_of_words / 180  # Вычисляем ср. время, при условии, что среднее время на чтение = 180 слов в минуту)
    #добавляем получившиеся результаты в лейбл
    amount_of_words.config(text=f"Количество слов в вашем тексте: {number_of_words}\nСреднее время его прочтения: {avg_reading_time} минут")

# функция с предобработкой текста перед построением облака слов
def preprocess_text_for_wordcloud(text):
    words = nltk.word_tokenize(text)     # токенизируем текст
    # Лемматизируем с помощью .parse и .normal_form от pymorphy2, а также фильтруем стопслова
    lemmatized_words = [
        morph.parse(word)[0].normal_form for word in words
        if word.lower() not in stop_words and word.isalnum()
    ]
    return ' '.join(lemmatized_words) #возвращаем оцищенный текст

def wordcloud(text):
    # Обрабатываем текст для облака слов
    processed_text = preprocess_text_for_wordcloud(text)

    # Создаем облако слов
    wc = WordCloud(
        width = 700,
        height = 600,
        background_color = 'white',
        max_font_size = 200,
        random_state = 42
    )
    wc.generate(processed_text)
    wc.to_file("word_cloud.png") # и сохраняем результат

    # Выводим получившееся облако в интерфейс через PhotoImage
    img = PhotoImage(file = "word_cloud.png")
    canvas.itemconfig(wc_on_canvas, image = img)
    canvas.image = img

#общая функция, которая вызывает все остальные
def text_processing():
    text = open_file() # открываем файл
    if text:
        num_of_words(text)  # для подсчета слов
        wordcloud(text)  # для создания облака слов


# создаем пользовательский интерфейс
window = Tk()
window.title("О чем текст?")
window.geometry("1920x1080")

#создаем лейбл с описанием, что пользователю нужно делать
instruction = Label(text = "Нажмите на кнопку и загрузите ваш текст: ")
instruction.place(x = 20, y = 20, width = 250, height = 30)
instruction['bg'] = 'grey'

#создаем текстовый виджет, куда будет выводиться загруженный текст
text_widget = Text(window)
text_widget.place(x = 800, y = 100, width = 700, height = 650)

#создаем кнопку, после нажатия на которую начинается весь процесс
button = Button(window, text = "Нажмите и выберите текстовый файл", command = text_processing)
button.place(x = 20, y = 60, width = 250, height = 30)

#создаем лейбл, куда выводится среднее количество слов, а также время прочтения
amount_of_words = Label(text = "")
amount_of_words.place(x = 10, y = 100, width = 350, height = 50)

#создаем канву, куда будет накладываться изображения облака слов
canvas = Canvas(window, width = 700, height = 600)
canvas["bg"] = "white"
wc_on_canvas = canvas.create_image(0, 0, anchor = "nw")
canvas.place(x = 10, y = 150)

window.mainloop()