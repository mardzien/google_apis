# operations on files


def load_file_to_list(filename):
    result = []
    with open(filename, encoding='utf-8') as fh:
        for line in fh:
            clean_line = line.replace("\n", "")
            result.append(f'{clean_line}')
    return result


def write_list_to_file(input_list, filename):
    with open(filename, 'w', encoding='utf-8') as fh:
        for element in input_list:
            fh.write(f"{element}\n")


def load_file_to_string(filename):
    result = ''
    with open(filename, encoding='utf-8') as fh:
        for line in fh:
            clean_line = line.replace("\n", "")
            result += f'{clean_line}, '
    return result
