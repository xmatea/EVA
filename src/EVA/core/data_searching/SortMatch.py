def SortMatch(results):
    # Sort the match results and counting the number of elements and return top five

    element_list = []

    for line in results:
        row = [line['peak_centre'], line['energy'], line['element'],
               line['transition'], line['error'], line['diff']]

        element_list.append(row[2])

    # Count number of elements
    counts = {element: element_list.count(element) for element in element_list}

    #sort the counts
    counts_sorted = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    #return top 5
    return dict(list(counts_sorted.items())[0:5])

