# Ancient_OTP | easy | crypto

### Сложность
easy

### Информация
Это и так лёгкий таск, вы справитесь без подсказок

### Выдасть участникам
Все, что в папке public: файл ecnrypt.py и output

### Решение
В таске происходит xor флага со случайной гаммой. Для решения нужно ее восстановить. 
Заметим, что в таске гамма шифруется с помощью Афинного шифра, и при этом сами параметры отдаются, 
то есть, мы можем восстановить исходную гамму.
Берём параметры a, b, m и по формуле $a^{-1} \cdot (x - b) \mod m$ находим гамму. Так как ciphertext был получен 
через xor флага и гаммы, то найденную гамму можно проксорить с ciphertext, чтобы восстановить значение flag.

```
python3 sploit.py
```

### Флаг
ctf{very_authentic_flag}