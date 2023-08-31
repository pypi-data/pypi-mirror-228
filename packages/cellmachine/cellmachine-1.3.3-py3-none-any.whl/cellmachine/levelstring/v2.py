from ..level import Level
from ..cells import *

base74_key = {char: index for index, char in enumerate("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&+-.=?^{}")}
base74_encodes = list(base74_key.keys())

def base74_decode(string):
    result = 0
    for char in string:
        result *= 74
        result += base74_key[char]
    return result

def base74_encode(num):
    if num < 74: return base74_encodes[num]
    
    result = ""
    while num:
        result = base74_encodes[num % 74] + result
        num = num // 74
    return result

# data){distance}
# data(distance)
#    ^ cell

def decode_data(encoded_data):
    decoded_data = []

    current_index = 0
    while current_index < len(encoded_data):
        if encoded_data[current_index] in "()":
            if encoded_data[current_index] == ")":
                for _ in range(base74_decode(encoded_data[current_index + 1])):
                    decoded_data.append(encoded_data[current_index - 1])
                current_index += 2
            else:
                cell = encoded_data[current_index - 1]
                distance = ""
                current_index += 1
                while encoded_data[current_index] != ")":
                    distance += encoded_data[current_index]
                    current_index += 1
                
                for _ in range(base74_decode(distance)):
                    decoded_data.append(cell)
                current_index += 1
        else:
            decoded_data.append(encoded_data[current_index])
            current_index += 1

    return decoded_data

def format_cells(decoded_data, width, height):
    placeables = set()
    cells = []

    celltype = {
        0: Generator,
        1: CW,
        2: CCW,
        3: Mover,
        4: Slide,
        5: Push,
        6: Immobile,
        7: Enemy,
        8: Trash,
        9: "BGDefault",
        10: "0",
    }

    for index, cell in enumerate(decoded_data):
        cell = base74_decode(cell)

        if cell % 2 == 1:
            x, y = index % width, index // width
            y = height - int(y) - 1
            placeables.add((x, y))
        if cell >= 72:
            continue
        x, y = index % width, index // width
        y = height - int(y) - 1
        _type, _rotation = (cell // 2) % 9, cell // 18

        cells.append(celltype[_type](None, (x, y), _rotation))

    return placeables, cells

def import_level(level_string):
    string_components = level_string.split(";")

    components = {
        'version': string_components[0],
        'width': base74_decode(string_components[1]),
        'height': base74_decode(string_components[2]),
        'data': string_components[3],
        'tutorial_text': string_components[4],
        'name': string_components[5],
    }

    decoded_data = decode_data(components['data'])
    placeables, cells = format_cells(decoded_data, components['width'], components['height'])

    level_data = {
        'size': (components['width'], components['height']),
        'placeables': placeables,
        'cells': cells,
        'tutorial_text': components['tutorial_text'],
        'name': components['name'],
    }

    lvl = Level(
        size=level_data['size'],
        cells=level_data['cells'],
        placeables=level_data['placeables'],
        name=level_data['name'],
        tutorial_text=level_data['tutorial_text'],
    )

    return lvl

def export_level(level):
    celltype = {
        "generator": 0,
        "cw": 1,
        "ccw": 2,
        "mover": 3,
        "slide": 4,
        "push": 5,
        "immobile": 6,
        "enemy": 7,
        "trash": 8,
        "BGDefault": 9,
        "0": 10,
    }

    cell_data = [72] * (level.size[0] * level.size[1])
    
    for placeable in level.placeables:
        cell_data[placeable[0] + ((level.size[1] - placeable[1] - 1) * level.size[0])] = 73
        
    for cell in level.cells.values():
        cell_data[cell.position[0] + \
            ((level.size[1] - cell.position[1] - 1) * level.size[0])] += \
            (2 * celltype[cell.celltype]) + (18 * cell.rotation) - 72
    
    run_length = 1
    
    cells = ""
    
    for data_index, cell_value in enumerate(cell_data):
        if data_index + 1 < len(cell_data) and cell_value == cell_data[data_index + 1]:
            run_length += 1
        else:
            if run_length > 3:
                encoded = base74_encode(run_length - 1)
                if len(encoded) > 1:
                    cells += base74_encodes[cell_value] + "(" + encoded + ")"
                else:
                    cells += base74_encodes[cell_value] + ")" + encoded
            else:
                cells += base74_encodes[cell_value] * run_length
            run_length = 1

    level_string = f'V2;{base74_encode(level.size[0])};{base74_encode(level.size[1])};{cells};{level.tutorial_text};{level.name}'

    return level_string
