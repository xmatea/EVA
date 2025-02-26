def sort_match(results: list[dict]) -> dict:
    """
    Finds top 6 most frequently occurring elements in the input list of dictionaries.

    Args:
        results: list of result dictionaries

    Returns:
        Dict of length 6, ordered by frequency. Dict key is element name, value is number of occurrences.
    """

    element_list = []

    for line in results:
        row = [line['peak_centre'], line['energy'], line['element'],
               line['transition'], line['error'], line['diff']]

        element_list.append(row[2])

    # Count number of elements
    counts = {element: element_list.count(element) for element in element_list}

    #sort the counts
    counts_sorted = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    #return top 6
    return dict(list(counts_sorted.items())[0:5])

