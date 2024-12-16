from io import BytesIO
from PIL import Image

# Загрузка изображений
background = Image.open('img/clear_field.png')
selected_box = Image.open('img/selected_box.png')
hit = Image.open('img/hit.png')
miss = Image.open('img/miss.png')
destroy = Image.open('img/destroy.png')

#Отрисовки игрового поля на основе данных в двумерном массиве `fields`.Двумерный массив (6x6), содержит информацию о состоянии каждой ячейки поля.
      #Значения:
# - '1', '2', '3', '4' - выделенная ячейка
#- '5' - попадание
#- '6' - уничтожение корабля
#- '7' - промах
#- другие значения - пустая ячейка
async def draw_field(field):
    img_field = background.copy()
    for i in range(6):
        for j in range(6):
            x = 50 + j * 100 - 5 * j
            y = 50 + i * 100 - 5 * i
            if field[i][j] in ('1', '2', '3', '4', '5', '6'):
                img_field.paste(selected_box.convert('RGB'), (x, y), selected_box)
            if field[i][j] == '5':
                img_field.paste(hit.convert('RGB'), (x, y), hit)
            if field[i][j] == '6':
                img_field.paste(destroy.convert('RGB'), (x, y), destroy)
            if field[i][j] == '7':
                img_field.paste(miss.convert('RGB'), (x, y), miss)
    with BytesIO() as io:
        img_field.save(io, "PNG")
        io.seek(0)
        return io.getvalue()
