def get_input_columns(picture_size, channels='rgb'):
    """
    Nombres de las columnas de datos que vamos a usar como "entradas".
    """
    input_columns = []
    for color in channels:
        input_columns.extend(['%s%i' % (color, i)
                              for i in range(picture_size ** 2)])

    return input_columns


