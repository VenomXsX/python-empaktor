def transform_bwt(data: str) -> str:
    data = data.strip()
    # EOF character
    data += "$"
    table = []
    for i in range(len(data)):
        data = data[-1] + data[:-1]
        table.append(data)
    table = sorted(table)
    output = ""
    for i in range(len(table)):
        output += table[i][-1]
    return output


def inverse_bwt(transformed_data: str) -> str:
    table = [""] * len(transformed_data)
    # add column
    for i in range(len(transformed_data)):
        table = [transformed_data[i] + table[i]
                 for i in range(len(transformed_data))]
        table = sorted(table)
    output = [row for row in table if row.endswith("$")][0].rstrip("$")
    return output
