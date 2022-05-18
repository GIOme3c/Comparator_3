# Comparator-v.2.0
########################################ENGLISH#################################
Q1 - How i can launch Comparator?
A1 - Double click on *.exe file in "dict" folder. if *.exe file or "dict" folder not exists download actual python version -> run terminal(ctrl+r -> write "cmd" -> press "enter") -> write:
"venv\Scripts\activate
python build.py". 
try again
*For Linux and MacOS users - check Q4

Q2 - Black/White list - how it works?
A2 - Black list hides rows, where file name includes some key words(More detailed in Q3). White list shows only rows, where file name includes some key words(More detailed in Q3).

Q3 - How i can use regular expressions?
A3 - Examples:
        Black list ".+/text.tst$" - hides all files, named "text.tst" in all directories (1/2/3/text.tst, 2/3/text.tst, d:/programms/files/text.tst)
        Black list ".+/text/.+" - hides all files, contaned in subfolder "text" (1/text/3/somefile.tst, 2/text/somefile.tst, /programms/files/text/somefile.tst)
        Black list "^/text/.+" - hides all files, contaned in folder "text" (text/1/2/somefile.sf, text/2/somefile.sf, text/somefile.sf)
    Base rules:
        . - any symbol
        + - multiple repetition of the previous symbol
        ^ - start of the string
        $ - end of the string
    All about regular expressions in python - https://docs.python.org/3/library/re.html
    Test your regular expression - https://regex101.com/r/vhuHtH/1
        
Q4 - How i can run not compile version of programm?
A4 - Download actual python version -> run terminal -> write "venv/Scripts/activate" -> write python Launch_Comparator.py.

########################################РУССКИЙ#################################
Q1 - Как я могу запустить Comparator?
A1 - Дважды щелкните по файлу *.exe в папке "dict". если файл *.exe или папка "dict" не существуют, загрузите актуальную версию python -> запустите терминал (ctrl+r -> напишите "cmd" -> нажмите "enter") -> напишите:
"venv\Scripts\activate
python build.py".
*Для пользователей Linux и macOS - смотреть Q4

Q2 - Black/White list - как это работает?
A2 - Black list скрывает строки, в которых имя файла содержит некоторые ключевые слова (подробнее в Q3). White list показывает только строки, где имя файла содержит некоторые ключевые слова (подробнее в Q3).

Q3 - Как я могу использовать регулярные выражения?
A3 - Примеры:
Black list ".+/text.tst$" - скрывает все файлы с именем "text.tst" во всех каталогах (1/2/3/text.tst, 2/3/text.tst, d:/programms/files/text.tst )
Black list ".+/text/.+" - скрывает все файлы, содержащиеся во вложенной папке "text" (1/text/3/somefile.tst, 2/text/somefile.tst, /programms/files/text/somefile.tst)
Black list "^/text/.+" - скрывает все файлы, содержащиеся в папке "text" (текст/1/2/ somefile.sf, текст/2/somefile.sf, текст/somefile.sf)
Базовые правила:
"." - любой символ
"+" - многократное повторение предыдущего символа
"^" - начало строки
"$" - конец строки
Все о регулярных выражениях в python - https://docs.python.org/3/library/re.html
Проверьте свое регулярное выражение - https://regex101.com/r/vhuHtH/1

Q4 - Как я могу запустить не скомпилированную версию программы?
A4 - Загрузить актуальную версию python -> запустить терминал -> написать "venv/Scripts/activate" -> написать python Launch_Comparator.py .