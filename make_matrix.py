import csv
import itertools
import sys
def get_stud_row():
    with open('stud_aoi_real.csv','r') as f:
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



#def some_name(alpha,max_count,gamma):
def some_name(alpha,max_count,gamma):
    #test_graph = 200 - gamma*int(row[0])
    alf = int(alpha)
    gamma = int(gamma) 
    print alf,max_count,gamma
    #max_count = 4
    no_of_committees = 15
    no_of_students = 150
    list_alpha,list_one_minus_alpha = segregate_edges()
    aoe_comm_dict,avg_outdegree = find_avg_outdegree()
    #print len(aoe_comm_dict)
    #matrix = [[1]*max_count*len(aoe_comm_dict) for _ in range(max_count*len(aoe_comm_dict))]
    matrix = [[1]*no_of_committees*max_count for _ in range(no_of_students)]
    aoe_comm_list = get_aoe_comm_list()
    #print aoe_comm_list
    #pref_graph=[300,200,100,50]
    pref_graph=[500,400,100,10]
    for row in get_stud_row():
        test_graph = 20 - gamma*int(row[0])/10
        #test_graph = 1
        for aoe in row[1:]:
            index_in_comm_list = find_aoe_comm_index(aoe_comm_list,aoe)
            try:
                for comm in aoe_comm_list[index_in_comm_list][1:]:
                    #print aoe,comm
                    #char = aoe
                    #comm = elem
                    for i in range(1,len(pref_graph)+1):
                        if row[i] == aoe :
                            if (row[0],aoe) in list_alpha:                          
                                if  matrix[int(row[0])-1][(int(comm)-1)*max_count] < test_graph*pref_graph[i-1]*alf*(len(aoe_comm_list[index_in_comm_list])-1):
                                    for j in range(max_count):
                                        matrix[int(row[0])-1][(int(comm)-1)*max_count + j] = test_graph*pref_graph[i-1]*alf*(len(aoe_comm_list[index_in_comm_list])-1)
                                break
                            else:
                                if matrix[int(row[0])-1][(int(comm)-1)*max_count] < test_graph*pref_graph[i-1]*(10-alf)*(len(aoe_comm_list[index_in_comm_list])-1):
                                    for j in range(max_count):
                                        matrix[int(row[0])-1][(int(comm)-1)*max_count + j] = test_graph*pref_graph[i-1]*(10-alf)*(len(aoe_comm_list[index_in_comm_list])-1)
                                break
            except TypeError:
                #print str(e)
                pass




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
    #print aoe_comm_dict,avg_outdegree,len(aoe_comm_dict)



def segregate_edges():
    aoe_comm_dict,avg_outdegree = find_avg_outdegree()
    list_alpha = []
    list_one_minus_alpha = []
    with open('stud_aoi_real.csv','r') as f:
        output = csv.reader(f,delimiter = ' ')
        for row in output:
            for num in row[1:]:
                try:
                    if aoe_comm_dict[num]>avg_outdegree:
                        list_one_minus_alpha.append((row[0],num))
                    else:
                        list_alpha.append((row[0],num))
                except KeyError:
                    #print str(e)
                    pass
    #print list_alpha
    return (list_alpha,list_one_minus_alpha)
    #print list_alpha,list_one_minus_alpha
    #print list_one_minus_alpha


def find_aoe_comm_index(aoe_comm_list,elem):
    for i,lst in enumerate(aoe_comm_list):
        if elem == lst[0]:
            return i







def make_matrix():
    some_name(alpha,max_count,gamma)
    #find_avg_outdegree()
    #segregate_edges()



    



if __name__ == '__main__':
    #some_name(sys.argv[1],sys.argv[2],sys.argv[3])
    make_matrix()
    #get_stud_row()
    #get_aoe_comm_list()
