def group_by(data: list, to_field: str, by: tuple) -> dict:
    output = {}
    fields_to_add = set(data[0].keys()) - set(by)
    for field in by:
        output[field] = data[0][field]
    output[to_field] = []
    for row in data:
        output[to_field].append({k: row[k] for k in fields_to_add})

    return output


def many_group_by(data: list, to_field: str, by: tuple) -> list:
    indexed = {}
    unique = by[0]
    output = []
    fields_to_add = set(data[0].keys()) - set(by)
    i = 0
    for row in data:
        if not row[unique] in indexed:
            indexed[row[unique]] = i
            body = {k: row[k] for k in by}
            body[to_field] = []
            output.append(body)
            i += 1
    print(indexed)
    for row in data:
        if any([row[k] for k in fields_to_add]):
            output[indexed[row[unique]]][to_field].append(
                {k: row[k] for k in fields_to_add if row[k] is not None}
            )

    return output
