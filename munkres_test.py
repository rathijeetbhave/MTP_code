from munkres import Munkres,print_matrix
import make_matrix
import sys
#import itertools
import csv

class student:
    """
    Creates a student class which is used to display all student information in output.
    """

    def __init__(self,s_no,Applicant_ID,name,category_applied,physical_disability,specialisation,part_a_marks,part_b_marks,total_marks,pref):
	#self.marks=marks
	self.name=name
	self.pref=pref
	self.s_no = s_no
        self.Applicant_ID = Applicant_ID
        self.category_applied = category_applied
        self.physical_disability = physical_disability
        self.specialisation = specialisation
        self.part_a_marks = part_a_marks
        self.part_b_marks = part_b_marks
        self.total_marks = total_marks
        

def create_stud_database():
    """
    Creates a student database with all required information of students.
    The first element of tuple indexes returned by the munkres.py file is used as key 
    to this dictionary to print all the required information about that student in 
    output along with his alloted committee.

    :rtype: Dictionary
    :return: A dictionary with serial number as key and list of 
	     all information about that student as value.
    """

    stud_list = []
    stud_dict = {}
    with open('phd_show_2015may_finaldone.csv','r') as f:
        output = csv.reader(f,delimiter = ',')
        for i,row in enumerate(output):
            stud_list.append(student(i,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8:]))
    #for stud in stud_list:
	    #print stud.marks,stud.name,stud.pref,stud.s_no+1
        #stud_list.sort(key = lambda student:student.marks,reverse=True)
        #stud_list.sort(key = lambda student:student.marks)
        #for stud in stud_list:
        #    print stud.name,stud.marks
        for stud in stud_list:
            stud_dict[stud.s_no] = [stud.Applicant_ID,stud.name,stud.category_applied,stud.physical_disability,stud.specialisation,stud.part_a_marks,stud.part_b_marks,stud.total_marks,stud.pref]
        #print stud_dict
        #for stud in stud_dict:
            #print stud.s_no,stud.name,stud.marks
        return stud_dict
        #print stud_dict


def munkres_test(alpha,max_count,gamma):
    """
    Prints the required output in the terminal. 
    Used to input the marix in weight maximisation algorithm. 
    Also prints the number of unassigned students along with their information and 
    also those students who have got alloted for either their third or fourth preferance. 
    Also prints the running count of each committee in form of a dictionary.

    **IMPORTANT**: We have to manually update the *no_of_committees* variable for different input files.
    

    :Parameters:
        alpha : Integer between 1-9
                This value specifies how much importance is to be given to load balancing
                and how much to be given to preferances of students. 
                Value of one means maximum importance to load balencing while
                value of 9 means maximum importance to student preferances.

                **WARNING**: Code does not work for values other than between one to nine.

        max_count : Integer
                    Maximum number of students per committee.

        gamma : Integer between 1-9
                This specifies how much importance is given to student marks.
                Value of one means little importance.
                Value of nine means very high importance.

    :rtype: NONE

    """

    print '\n'
    print "You chose alpha = %s (more alpha value means higher importance to student preferances (at cost of more imbalence in committee loads). Choose *lower* but positive alpha if balencing is priority." %(alpha)

    print '\n'

    print "%s is the (hard constraint) maximun number of students per committee" %(max_count)

    print '\n'

    print "%s is the gamma value. It has to be between 1-9. Higher value means greater decrease in importance of test performance of successive students when alloting." %(gamma)

    print '\n'

    print "Number of committees being read from --csv file--: no. of committees"
    print "Number of students being read form --csv file-- : no. of students"
    print '\n'

    print "building weights matrix: rows = %d and columns = %d" 

    m=Munkres()
    no_of_committees = 20
    #matrix=[[5,9,1],[10,3,2],[8,7,4]]
    #matrix=[[100,102,1,1],[100,102,1,1],[200,200,202,202],[200,200,202,202]]
    #matrix=[[20,160,1,1],[1,80,40,1],[20,1,1,160],[1,80,40,1]]
    stud_dict = create_stud_database()
    #print stud_dict
    matrix = make_matrix.some_name(alpha,int(max_count),int(gamma))
    cost_matrix = []
    for row in matrix:
        cost_row = []
        for col in row:
                cost_row += [sys.maxsize - col]
        cost_matrix += [cost_row]
    indexes=m.compute(cost_matrix)
    #print indexes

    unassigned = count_unassigned(indexes,matrix,stud_dict)
    unwanted = unwanted_assignments(indexes,stud_dict,max_count)
    count_dict = generate_count(indexes,no_of_committees,matrix,max_count)


    #for row,tuples in itertools.izip(make_matrix.get_stud_row(),indexes):
        ##print row,tuples
        #print row.index(tuples[
        
    #print_matrix(matrix, msg='Lowest cost through this matrix:')
    total = 0
    with open('final_allotment.csv','w') as f:
	    for row, column in indexes:
		    value = matrix[row][column]
		    total += value
		    #print '(%d, %d) -> %d' % (row, column, value)
		    #print stud_dict[row]+[,],column/int(max_count)+1,value
		    f.write(str(stud_dict[row]) + ',' + str(column/int(max_count)+1) + ',' + str(value) + '\n')
		    #print stud_dict[row],column/int(max_count)+1,value
    
    print "Number of students not alloted any committee = ",unassigned
    print "Number of students getting 3rd or worse choice = ",unwanted
    print "Total number of students alloted some committee = ", len(indexes)-unassigned
    #print count_dict
    for comm,num in count_dict.items():
	    print "Committee %d : %d" %(comm,num)

        

    #print 'total cost: %d' % total



def count_unassigned(indexes,matrix,stud_dict):
    """
    Counts the number of unassigned students.

    :Parameters:
        indexes : list of tuples
            The output of munkres.py file

        matrix : list of lists
            matrix containing the cost of each path from student to committee.
            this is the output of make_matrix.py file.

        stud_dict : dictionary
            Dictionary of students with serial number as keys 
            and array of other related information as values.

    :rtype: Integer
    :return: The number of unassigned students.

    """

    unassigned = 0
    for row,col in indexes:
        if matrix[row][col] == 1:
            unassigned += 1
            try:
                print stud_dict[row] 
            except TypeError:
                pass
    print '\n'
    return unassigned

def get_stud_row():
    """
    returns a list of lists of student data along with their preferances.
    Each row contains the serial number of student along with his four preferances.

    final_stud_file.csv : Comma seperated values with first column as serial number
    and rest of the four columns containing the four preferances.
    name of input file with student data.

    :rtype: list of lists
    :return: List of lists of student serial number along with their preferances.

    """
    
    stud_list = []
    with open('final_stud_file.csv','r') as f:
        output = csv.reader(f,delimiter = ',')
        for row in output:
            stud_list.append(row)
    return stud_list
                                            

def unwanted_assignments(indexes,stud_dict,max_count):
    """
    Find only those assignments in which student have got either his thire or fourth preferance.
    The number of such students is preferred to be around five percent of total students.
    This function prints those students along with their complete information on terminal.
    :Parameters:
        indexes : list of tuples
            The output of munkres.py file

        stud_dict : dictionary
            Dictionary of students with serial number as keys and array of other related information as values.

        max_count : Integer
            Maximum number of students per committee.
            

    :rtype: Integer
    :return: Total number of students who got alloted for either third or fourth preferance.

    """

    stud_list = get_stud_row()
    unwanted = 0
    aoe_comm_list = make_matrix.get_aoe_comm_list()
    #print aoe_comm_list
    #stud_list = get_stud_row() 
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
                        if (comm/int(max_count)+1)== int(committee):
                            if _list.index(elem)>1:
                                #print elem,comm/10
                                #print _list.index(elem)
                                print stud_dict[stud],comm/int(max_count)+1,elem
                                unwanted += 1
                                flag = 1
                                break
                            else:
                                flag = 1
                                break
                    #else:
                        #if (comm/10+1)== int(committee):
                            #if _list.index(elem)>1:
                                ##print elem,comm/10
                                ##print _list.index(elem)
                                #print stud_dict[stud],comm/10+1,elem
                                #unwanted += 1
                                #flag = 1
                                #break
                            #else:
                                #flag = 1
                                #break



            except TypeError:
                pass

            if flag ==1:
                break
    print '\n'
    print '\n'

    return unwanted   

def generate_count(indexes,no_of_committees,matrix,max_count):
    """
    Generates a dictionary of committees with the number of students alloted to it.

    :Parameters:
        indexes : list of tuples
            The output of munkres.py file

        no_of_committees : Integer
            The total number of committees.

        matrix : list of lists
            matrix containing the cost of each path from student to committee.
            this is the output of make_matrix.py file.

    :rtype: dictionary
    :return: Dictionary with number of students assigned to different committees.

    """

    count_dict = {}
    for i in range(no_of_committees):
	count_dict[i+1] = 0

    for stud,comm in indexes:
	if matrix[stud][comm] != 1:
	    count_dict[comm/int(max_count)+1] += 1
    return count_dict


def make_name_dict():
    with open('namefile.txt','r') as f:
        output = csv.reader(f,delimiter = ' ')
        for i,row in enumerate(output):
            name_dict[i] = row
    return name_dict
        
        


if __name__ == '__main__':
    munkres_test(sys.argv[1],sys.argv[2],sys.argv[3])
    #create_stud_database()
