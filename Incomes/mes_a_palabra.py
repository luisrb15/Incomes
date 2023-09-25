def mes_a_palabra(mes_numero):
    mes_dic = {
        '1' : 'Enero',
        '2' : 'Febrero',
        '3' : 'Marzo',
        '4' : 'Abril',
        '5' : 'Mayo',
        '6' : 'Junio',
        '7' : 'Julio',
        '8' : 'Agosto',
        '9' : 'Septiembre',
        '10' : 'Octubre',
        '11' : 'Noviembre',
        '12' : 'Diciembre'
    }
    
    for key, value in mes_dic.items():
        if  key == str(mes_numero):
            mes_palabra = value
    return mes_palabra