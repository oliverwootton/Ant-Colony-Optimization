
def file_read(filename):
  
    with open(filename) as f:
        n = int(f.readline()) # read first line
        D = []
        F = []
        x = 0
        for line in f: # read rest of lines
            if line.split() == []:
                x += 1
                continue
            elif x < 51:
                D.append([int(x) for x in line.split()])
            else:
                F.append([int(x) for x in line.split()])
            x += 1

    return(n, D, F)