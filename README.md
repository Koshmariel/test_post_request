Челлендж: написать автоматический тест, который сможет найти любой из обнаруженных вами дефектов.

В качестве бага для проверки я выбрал задачу, с которой до этого не сталкивался - отправку POST запроса с данными из заполненных форм.

Мой подход к решению задачи: перехват всех запросов (заголовков и их тел при помощи BrowserMobProxy). Т.к. спецификация отсутствует, то парсить лог в поисках нужного запроса и извлекать его не имеет смысла т.к. его всё равно не получиться сравнить с эталоном, котороый отсутсвует. Но если POST-запрос уходит, значит в его теле должны содержаться данные, введённые в поля. Т.о. можно ввести в поля определённые последовательности символов, представить лог прокси-сервера в виде строки и искать в ней вхождения этих подстрок.

Фыйлы:

test_approach.py - проверка подхода на сайте, с работотающей отправкой данных, введённых в форму

test_approach_with_pytest.py - адаптация кода для pytest

check_with_pytest.py - проверка отправки данных со странициы в тестовом задании
