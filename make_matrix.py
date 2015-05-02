import csv
import itertools
import sys
def get_stud_row():
    with open('stud_aoi_real_1.csv','r') as f:
        output = csv.reader(f,delimiter = ' ')
        for row in output:
            yield row


def get_aoe_comm_list():
    aoe_comm_list = []
    with open('aoi_comm_real.csv','r') as f:
        output = csv.reader(f,delimiter = ' ')
        for line in output:
            aoe_comm_list.append(line)
    return aoe_comm_list



def some_name(alpha,max_count,gamma):
    #test_graph = 200 - gamma*int(row[0])
    alf = int(alpha)
    list_alpha,list_one_minus_alpha = segregate_edges()
    aoe_comm_dict,avg_outdegree = find_avg_outdegree()
    matrix = [[1]*max_count*len(aoe_comm_dict) for _ in range(max_count*len(aoe_comm_dict))]
    aoe_comm_list = get_aoe_comm_list()
    pref_graph=[300,200,100]
    for row in get_stud_row():
        test_graph = 20 - gamma*int(row[0])/10
        #test_graph = 1
        for char in row[1:]:
            for elem in aoe_comm_list[int(char[0])-1][1:]:
                for i in range(1,len(pref_graph)+1):
                    if row[i] == char :
                        if (row[0],elem) in list_alpha:                          
                            if  matrix[int(row[0])-1][(int(elem[0])-1)*max_count] < test_graph*pref_graph[i-1]*alf*(len(aoe_comm_list[int(char)-1])-1):
                                for j in range(max_count):
                                    matrix[int(row[0])-1][(int(elem[0])-1)*max_count + j] = test_graph*pref_graph[i-1]*alf*(len(aoe_comm_list[int(char)-1])-1)
                        else:
                            if matrix[int(row[0])-1][(int(elem[0])-1)*max_count] < test_graph*pref_graph[i-1]*(10-alf)*(len(aoe_comm_list[int(char[0])-1])-1):
                                for j in range(max_count):
                                    matrix[int(row[0])-1][(int(elem[0])-1)*max_count + j] = test_graph*pref_graph[i-1]*(10-alf)*(len(aoe_comm_list[int(char[0])-1])-1)




    #for row in matrix:
        #print row
    return matrix


def find_avg_outdegree():
    out_degree = 0
    total_committees = 0
    aoe_comm_dict = {}
    _sum = 0
    with open('aoi_comm_real.csv','r') as f:
        output = csv.reader(f,delimiter = ' ')
        for row in output:
            aoe_comm_dict[row[0]] = int(len(row[1:]))

    for i in aoe_comm_dict.values():
        _sum += i
    avg_outdegree = _sum/len(aoe_comm_dict)
    return (aoe_comm_dict,avg_outdegree)
    #print aoe_comm_dict,avg_outdegree



def segregate_edges():
    aoe_comm_dict,avg_outdegree = find_avg_outdegree()
    list_alpha = []
    list_one_minus_alpha = []
    with open('stud_aoi_real_1.csv','r') as f:
        output = csv.reader(f,delimiter = ' ')
        for row in output:
            for num in row[1:]:
                try:
                    if aoe_comm_dict[num]>avg_outdegree:
                        list_one_minus_alpha.append((row[0],num))
                    else:
                        list_alpha.append((row[0],num))
                except Exception,e:
                    print str(e)
    return (list_alpha,list_one_minus_alpha)
    #print list_alpha,list_one_minus_alpha
    #print list_one_minus_alpha





def make_matrix():
    some_name(alpha,max_count)
    #find_avg_outdegree()
    #segregate_edges()



    



if __name__ == '__main__':
    #some_name(sys.argv[1],sys.argv[2])
    make_matrix()
    #get_stud_row()
    #get_aoe_comm_list()
