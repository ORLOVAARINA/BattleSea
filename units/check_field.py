#Проверка, содержит ли поле (представленное двумерным списком (fields)) значения 1, 2, 3 или 4.
def check_field(field):
    for row in field:
        for element in row:
            if int(element) in (1, 2, 3, 4):
                return True
    return False