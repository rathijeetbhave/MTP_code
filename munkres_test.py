from munkres import Munkres,print_matrix
import make_matrix
import sys
import itertools

def munkres_test(alpha,max_count,gamma):
    m=Munkres()
    #matrix=[[5,9,1],[10,3,2],[8,7,4]]
    #matrix=[[100,102,1,1],[100,102,1,1],[200,200,202,202],[200,200,202,202]]
    #matrix=[[20,160,1,1],[1,80,40,1],[20,1,1,160],[1,80,40,1]]
    matrix = make_matrix.some_name(alpha,int(max_count),int(gamma))
    cost_matrix = []
    for row in matrix:
        cost_row = []
        for col in row:
                cost_row += [sys.maxsize - col]
        cost_matrix += [cost_row]
    indexes=m.compute(cost_matrix)
    #print indexes

    #for row,tuples in itertools.izip(make_matrix.get_stud_row(),indexes):
        ##print row,tuples
        #print row.index(tuples[
        
    print_matrix(matrix, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
            value = matrix[row][column]
            total += value
            print '(%d, %d) -> %d' % (row, column, value)

        

    print 'total cost: %d' % total




if __name__ == '__main__':
    munkres_test(sys.argv[1],sys.argv[2],sys.argv[3])
