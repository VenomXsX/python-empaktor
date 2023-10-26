def transform_bwt(data: str) -> str | int:
    data = data.strip()
    table = []
    for i in range(len(data)):
        data = data[-1] + data[:-1]
        table.append(data)
    table = sorted(table)
    key = table.index(data)
    output = ""
    for i in range(len(table)):
        output += table[i][-1]
    return output, key


def inverse_bwt(transformed_data: str, key: int) -> str:
    table = [""] * len(transformed_data)
    # add column
    for _ in range(len(transformed_data)):
        table = [transformed_data[i] + table[i]
                 for i in range(len(transformed_data))]
        table = sorted(table)
    output = table[key]
    return output
