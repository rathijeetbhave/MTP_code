from munkres import Munkres,print_matrix
import make_matrix
import sys
import itertools
import csv

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

    unassigned = count_unassigned(indexes,matrix)
    unwanted = unwanted_assignments(indexes)


    #for row,tuples in itertools.izip(make_matrix.get_stud_row(),indexes):
        ##print row,tuples
        #print row.index(tuples[
        
    #print_matrix(matrix, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
            value = matrix[row][column]
            total += value
            #print '(%d, %d) -> %d' % (row, column, value)
    
    print "unassigned =",unassigned
    print "unwanted =",unwanted

        

    #print 'total cost: %d' % total



def count_unassigned(indexes,matrix):
    unassigned = 0
    for row,col in indexes:
        if matrix[row][col] == 1:
            unassigned += 1
    return unassigned

def get_stud_row():
    stud_list = []
    with open('stud_aoi_real.csv','r') as f:
        output = csv.reader(f,delimiter = ' ')
        for row in output:
            stud_list.append(row)
    return stud_list
                                            

def unwanted_assignments(indexes):
    stud_list = get_stud_row()
    unwanted = 0
    aoe_comm_list = make_matrix.get_aoe_comm_list()
    #print aoe_comm_list
    stud_list = get_stud_row() 
    for stud,comm in indexes:
        flag = 0
        try:
            _list = stud_list[int(stud)][1:]
            #print _list
        except IndexError:
            pass
        for elem in _list:
            _index = make_matrix.find_aoe_comm_index(aoe_comm_list,elem)
            #print _index
            try:
                for committee in aoe_comm_list[_index][1:]:
                    if comm%10 == 0:                         # 140/10 =14 , 145/10 should be 15
                        if (comm/10)== int(committee):
                            if _list.index(elem)>1:
                                #print elem,comm/10
                                #print _list.index(elem)
                                print stud,comm/10,elem
                                unwanted += 1
                                flag = 1
                                break
                            else:
                                flag = 1
                                break
                    else:
                        if (comm/10+1)== int(committee):
                            if _list.index(elem)>1:
                                #print elem,comm/10
                                #print _list.index(elem)
                                print stud,comm/10+1,elem
                                unwanted += 1
                                flag = 1
                                break
                            else:
                                flag = 1
                                break



            except TypeError:
                pass

            if flag ==1:
                break

    return unwanted   
        
        


if __name__ == '__main__':
    munkres_test(sys.argv[1],sys.argv[2],sys.argv[3])
