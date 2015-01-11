def mergesort(*args):
    num_of_arrays = len(args)
    result = []
    if num_of_arrays == 1:
        return args[0]
    if num_of_arrays == 2:
        a = args[0]
        b = args[1]
        while a and b:
            if a[0] > b[0]:
                result.append(a.pop(0))
            else:
                result.append(b.pop(0))
        if a:
            result = result + a
        else:
            result = result + b
        return result
    else:
        for step in range(0, num_of_arrays - 1):
            result = mergesort(args[step], args[step + 1])
    return result

print mergesort(*[[3,2], [4,1]])
