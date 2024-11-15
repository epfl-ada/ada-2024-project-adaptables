def number_to_emoji(number: int):
    # Utilitary function to transform any number into a sequence of digit emojis
    # Used for artistic purposes only
    return ''.join([f'{chr(ord("0") + int(digit))}\uFE0F\u20E3' for digit in str(number)])
