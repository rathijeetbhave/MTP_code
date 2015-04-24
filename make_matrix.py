import csv
import itertools
import sys
def get_stud_row():
    with open('std_aoe_4.txt','r') as f:
        output = csv.reader(f,delimiter = ' ')
        for row in output:
            yield row


def get_aoe_comm_list():
    aoe_comm_list = []
    with open('aoe_comm_2.txt','r') as f:
        output = csv.reader(f,delimiter = ' ')
        for line in output:
            aoe_comm_list.append(line)
    return aoe_comm_list



def some_name(alpha,max_count):
    alf = int(alpha)
    list_alpha,list_one_minus_alpha = segregate_edges()
    aoe_comm_dict,avg_outdegree = find_avg_outdegree()
    matrix = [[1]*max_count*len(aoe_comm_dict) for _ in range(max_count*len(aoe_comm_dict))]
    aoe_comm_list = get_aoe_comm_list()
    for row in get_stud_row():
        for char in row[1:]:
            for elem in aoe_comm_list[int(char)-1][1:]:
                if row[1] == char:
                    if (row[0],elem) in list_alpha:
                        if  matrix[int(row[0])-1][(int(elem)-1)*max_count] < 300*alf*(len(aoe_comm_list[int(char)-1])-1):
                            for i in range(max_count):
                                matrix[int(row[0])-1][(int(elem)-1)*max_count + i] = 300*alf*(len(aoe_comm_list[int(char)-1])-1)
                    else:
                        if matrix[int(row[0])-1][(int(elem)-1)*max_count] < 300*(10-alf)*(len(aoe_comm_list[int(char)-1])-1):
                            for i in range(max_count):
                                matrix[int(row[0])-1][(int(elem)-1)*max_count+i] = 300*(10-alf)*(len(aoe_comm_list[int(char)-1])-1)

                elif row[2] == char:
                    if (row[0],elem) in list_alpha:
                        if matrix[int(row[0])-1][(int(elem)-1)*max_count] < 200*alf*(len(aoe_comm_list[int(char)-1])-1):
                            for i in range(max_count):
                                matrix[int(row[0])-1][(int(elem)-1)*max_count+i] = 200*alf*(len(aoe_comm_list[int(char)-1])-1)
                    else:
                        if matrix[int(row[0])-1][(int(elem)-1)*max_count] < 200*(10-alf)*(len(aoe_comm_list[int(char)-1])-1):
                            for i in range(max_count):
                                matrix[int(row[0])-1][(int(elem)-1)*max_count+i] = 200*(10-alf)*(len(aoe_comm_list[int(char)-1])-1)

                elif row[3] == char:
                    if (row[0],elem) in list_alpha:
                        if matrix[int(row[0])-1][(int(elem)-1)*max_count] < 100*alf*(len(aoe_comm_list[int(char)-1])-1):
                            for i in range(max_count):
                                matrix[int(row[0])-1][(int(elem)-1)*max_count+i] = 100*alf*(len(aoe_comm_list[int(char)-1])-1)
                    else:
                        if matrix[int(row[0])-1][(int(elem)-1)*max_count] < 100*(10-alf)*(len(aoe_comm_list[int(char)-1])-1):
                            for i in range(max_count):
                                matrix[int(row[0])-1][(int(elem)-1)*max_count+i] = 100*(10-alf)*(len(aoe_comm_list[int(char)-1])-1)


    #for row in matrix:
        #print row
    return matrix


def find_avg_outdegree():
    out_degree = 0
    total_committees = 0
    aoe_comm_dict = {}
    _sum = 0
    with open('aoe_comm_2.txt','r') as f:
        output = csv.reader(f,delimiter = ' ')
        for row in output:
            aoe_comm_dict[row[0]] = int(len(row[1:]))

    for i in aoe_comm_dict.values():
        _sum += i
    avg_outdegree = _sum/len(aoe_comm_dict)
    return (aoe_comm_dict,avg_outdegree)



def segregate_edges():
    aoe_comm_dict,avg_outdegree = find_avg_outdegree()
    list_alpha = []
    list_one_minus_alpha = []
    with open('std_aoe_4.txt','r') as f:
        output = csv.reader(f,delimiter = ' ')
        for row in output:
            for num in row[1:]:
                if aoe_comm_dict[num]>avg_outdegree:
                    list_one_minus_alpha.append((row[0],num))
                else:
                    list_alpha.append((row[0],num))
    return (list_alpha,list_one_minus_alpha)





def make_matrix():
    some_name(alpha,max_count)
    #find_avg_outdegree()
    #segregate_edges()



    



if __name__ == '__main__':
    some_name(sys.argv[1],sys.argv[2])
    #make_matrix()
    #get_stud_row()
    #get_aoe_comm_list()
