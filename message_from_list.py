def message_from_list(l):
    message = 'Наиболее вероятные варианты:\n'
    l = sorted(l, reverse=True, key=lambda a: a[1])
    message += '\n'.join([f'{i[0]} \t {i[1]}' for i in l])
    return message
