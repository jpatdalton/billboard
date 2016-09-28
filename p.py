
def func(arg1, *args, **kwargs):
    def test():
        print arg1
    print 'arg1', arg1
    print 'args', args
    print 'kwargs', kwargs

def fill_space(string, length):
    if string:
        string = '%20'.join(string[0:length].split())
    return string


def rotate90(image):
    length = len(image)
    for i in range(length/2):
        const = length-i-1
        for j in range(i,length-i-1):

            temp = image[i][j]
            image[i][j] = image[const-j][i]
            image[const-j][i] = image[const][const-j]
            image[const][const-j] = image[j][const]
            image[j][const] = temp
            print "##"+str(i)+"##"+str(j)+"###"
            print image[0]
            print image[1]
            print image[2]
            print image[3]
            print image[4]
            print '#########\n'
    print "Final"
    print image[0]
    print image[1]
    print image[2]
    print image[3]
    print image[4]
    print '#########\n'
    return image
rotate90([[j for j in range(5)] for i in range(5)])

image = [[i]*4 for i in range(4)]
im = [[j for j in range(4)] for i in range(5)]


def fill_zeroes(matrix):
    if matrix:
        rows = len(matrix)
        cols = len(matrix[0])
        cols_zero  = [False] * cols
        rows_zero = [False] * rows
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == 0:
                    rows_zero[i] = True
                    cols_zero[j] = True
    print rows_zero
    for i in range(len(rows_zero)):
        if rows_zero[i]:
            print 'i',i
            matrix[i][:] = [0 for x in range(cols)]
            print matrix
    print cols_zero
    for j in range(len(cols_zero)):
        if cols_zero[j]:
            print 'j',j
            for row in matrix:
                row[j] = 0
            print matrix
    return matrix

matrix = [[1, 1, 1, 0,2],
[1, 1, 1, 1,2],
[2, 0, 1, 2,2],
[3, 3, 3, 1,2],]

fill_zeroes(matrix)
