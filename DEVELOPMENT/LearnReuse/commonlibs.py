def sum_list(lst_input):
    ttl = 0
    for i in lst_input:
        ttl += i
    return ttl


def min_max_ttL_avg(lst_input):
    n = min(lst_input)
    m = max(lst_input)
    total = sum_list(lst_input)
    a = total / len(lst_input)
    return [n, m, total, a]

pi = 3.14159

def area(radius):
    return float(pi * radius * radius)

def parameter(radius):
    return 2 * pi * radius


def main():
    ## Unit test area for functions to be imported.
    lst_test = [1,2,3]
    print min_max_ttL_avg(lst_test)

    print "Unit test completed ..."


if __name__ == "__main__":
    main()