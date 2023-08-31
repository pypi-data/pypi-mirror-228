import os
import string


def without_special_characters_input(prompt: str) -> str:
    while True:
        result = input(prompt)
        if [
            letter
            for letter in result
            if letter not in string.ascii_letters + string.digits + ' '
        ]:
            input(
                (
                    'Não digite caracteres especiais. Aperte Enter para contin'
                    'uar...'
                )
            )
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            break
    return result
