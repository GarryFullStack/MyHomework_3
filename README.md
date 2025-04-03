# MyHomework_3 
## Практическое задание к Уроку №23 "Проект создание Игры"
### Цель создание проекта.
Вы будете создаваться игру, которая заключается в следующем:
Есть прямоугольное поле, на котором расположены деревья и реки.
Деревья периодически будут вырастать и периодически загораться.
Задача заключается в том, чтобы вовремя тушить эти деревья с помощью вертолета.
Вертолет перемещается по карте, пролетая над клеткой с водой он берет ее в резервуар и может потушить одно дерево.

# С п р а в к а :
Проект игры создан с помощью шаблонов библиотеки PyGame

### === Расстановка на игровом поле по цветам клеток: ===

Bертолет - жёлтая клетка <br />
Дерево - зелёная <br />
Дерево в огне - красная <br />
Реки - синяя <br />

### === Правила игры: ===

Вертолет  набирает воду из рек "пролетая" над ними и тушит горящие деревья сбрасывая воду. "Залетать" на огонь нельзя, иначе будет сгорать и уменьшаться количество жизней вертолета. Тушение производится  на касательной к огню позиции с любой стороны дерева.  На экран выводится статистика: количество жизней вертолета и потушенных деревьев,наличие воды. 

### === Управление клавиатурой: ===

Перемещения вертолета:
Вперед - "UP" <br />
Назад -  "DOWN" <br />
Вправо - "RIGHT" <br />
Влево -  "LEFT" <br />
Сброс воды - "SPACE"



