Открыв сайт можно увидеть тест на то, какой Вы персонаж из Игры Престолов. Попробуем выбрать различные варианты ответов и ввести свое имя. 

![My Image](https://raw.githubusercontent.com/bysmaks/baumanka_ctf/main/web/house_of_pain/solve/img/1.png?token=GHSAT0AAAAAACGPRNOYAU2AVJBCY3YX63USZRXXHFA)

Видим, что мы принадлежим дому Грейджоев. Раз здесь Flask и имя рендерится, то лучше всего попробовать поискать SSTI Jinja инъекцию.

![My Image](https://raw.githubusercontent.com/bysmaks/baumanka_ctf/main/web/house_of_pain/solve/img/2.png?token=GHSAT0AAAAAACGPRNOZAFF6HL4LC3I3KHCCZRXXDSA)

Рационально перейти в Burp Suite. Видим, что отправив фигурные скобки, нашу атаку блокируют.

![My image](https://raw.githubusercontent.com/bysmaks/baumanka_ctf/main/web/house_of_pain/solve/img/3.png?token=GHSAT0AAAAAACGPRNOYDRHDQOKTTMCL6DLMZRXXETA)

Видимо, мы действительно движемся в нужную сторону. Перебрав различные пэйлоады, понимаем, что фильтров там достаточно, надо почитать про другие методы байпасса. Вспоминаем про технику отправки многострочного запроса, другими словами \r\n. 
Действительно, кажется пэйлоад проходит. Пробуем найти другой, позволяющий прочитать файл. Читаем и сдаем флаг.

![My image](https://raw.githubusercontent.com/bysmaks/baumanka_ctf/main/web/house_of_pain/solve/img/4.png?token=GHSAT0AAAAAACGPRNOZYEHOLT6QXZEISIIQZRXXFTQ)

![My image](https://github.com/bysmaks/baumanka_ctf/blob/main/web/house_of_pain/solve/img/5.png)
