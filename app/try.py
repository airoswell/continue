def sd(y):
    mean_y = sum(y) / float(len(y))
    tot = 0.0
    for x in y:
        tot += (x-mean_y)**2
    return (tot/len(y))**0.5


sd(3)
