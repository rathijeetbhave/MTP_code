#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Documentation is intended to be processed by Epydoc.

"""
Introduction
============
This file is used to make the input matrix for the munkres algorithm.
It is like a helper file for munkres_test.py file

Description
===========

The input file with student information is read and each line in file is *yielded*.
The area/project to committee file is read and stored in form of list in aoe_comm_list.
The *some_name* function takes three parameters as input. *Alpha* for load balencing, *gamma*
for test performance and *pref_graph* which signifies how fast the importance of student 
preferances decreases. Pref_graph is hard coded in algorithm in the form of an array. We can see from the array that the weight significantly decreases for the third and fourth preferance.
It is set like that because we want maximum students to get either their first or second 
preferance.  Depending on the parameters that we set the, function assigns appropriate weights 
to all rows andcolumns which corresponds to students and committees respectively.

The average outdegree is calculated to identify the edges with more potential to do load 
balencing and increase their weights accordingly so that the likelihood of them being in the 
final assignment increases.  The edges are then divided in two groups depending on the average 
outdegree and appropriate weights are assigned to them to complete the matrix.

Copyright and License
=====================

This software is released under a BSD license, adapted from
<http://opensource.org/licenses/bsd-license.php>

Copyright (c) 2015 Rathijeet Bhave
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

"""

__docformat__ = 'restructuredtext'

#------------------------------------------------------------------------------------------
# Info about the module

__author__    = "Rathijeet Bhave, rathijeetbhave@gmail.com"
__copyright__ = "(c) 2008 Rathijeet Bhave"
__license__   = "BSD-style license"

#------------------------------------------------------------------------------------------

import csv
import itertools
import sys
#class student:
    #def __init__(self,s_no,name,marks,pref):
	#self.marks=marks
	#self.name=name
	#self.pref=pref
	#self.s_no = s_no
#
#def create_stud_database():
    #stud_list = []
    #with open('stud_and_marks.csv','r') as f:
        #output = csv.reader(f,delimiter = ',')
        #for i,row in enumerate(output):
		#stud_list.append(student(i,row[0],row[1],row[2:]))
    ##for stud in stud_list:
	    ##print stud.marks,stud.name,stud.pref,stud.s_no+1
        #stud_list.sort(key = lambda student:student.marks)

	

					    
def get_stud_row():
    """
    Yield rows of student data one by one.
    Each row contains the serial number of student along with his four preferances.

    final_stud_file.csv : Comma seperated values with first column as serial number
    and rest of the four columns containing the four preferances.
    name of input file with student data.

    :rtype: list
    :return: one row of input file at a time.

    """

    with open('final_stud_file.csv','r') as f:
        output = csv.reader(f,delimiter = ',')
        for row in output:
            yield row


def get_aoe_comm_list():
    """
    Returns a list of lists with area/project of intrest as first element 
    followed by all the committees that cover the specific area/project of intrest.

    aoi_comm_new.csv : CSV file with first column as area/project of intrest and rest 
    of columns as the committees that cover that area of intrest.

    :rtype: list of lists
    :return: list of lists of all area/project of intrest along with their committees.

    """

    aoe_comm_list = []
    with open('aoi_comm_new.csv','r') as f:
        output = csv.reader(f,delimiter = ' ')
        for line in output:
            aoe_comm_list.append(line)
    return aoe_comm_list



#def some_name(alpha,max_count,gamma):
def some_name(alpha,max_count,gamma):
    """
    Forms the matrix that acts like an input to munkres.py.
    Returns a matrix in form of list of lists.

    :Parameters:
        alpha : Integer between 1-9
            This value specifies how much importance is to be given to load balancing
            and how much to be given to preferances of students. 
            Value of one means maximum importance to load balencing while
            value of 9 means maximum importance to student preferances.

            **WARNING**: Code does not work for values other than between one to nine.

        :rtype: list of lists
        :return: A list of lists as a matrix to be used as 
                 input for weight maximisation algorithm.

    """
    #test_graph = 200 - gamma*int(row[0])
    alf = int(alpha)
    gamma = int(gamma) 
    #print alf,max_count,gamma
    #max_count = 4
    no_of_committees = 20
    no_of_students = 148
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
            #print index_in_comm_list
            try:
                for comm in aoe_comm_list[index_in_comm_list][1:]:
                    #print aoe,comm
                    #char = aoe
                    #comm = elem
                    for i in range(1,len(pref_graph)+1):
                        if row[i] == aoe :
                            if (row[0],aoe) in list_alpha:                          
                                weight = test_graph*pref_graph[i-1]*alf*(len(aoe_comm_list[index_in_comm_list])-1)
                                if matrix[int(row[0])-1][(int(comm)-1)*max_count] < weight :
                                    for j in range(max_count):
                                        matrix[int(row[0])-1][(int(comm)-1)*max_count + j] = weight
                                break
                            elif (row[0],aoe) in list_one_minus_alpha:                          
                                weight = test_graph*pref_graph[i-1]*(10-alf)*(len(aoe_comm_list[index_in_comm_list])-1)
                                if matrix[int(row[0])-1][(int(comm)-1)*max_count] < weight :
                                    for j in range(max_count):
                                        matrix[int(row[0])-1][(int(comm)-1)*max_count + j] = weight
                                break
            except TypeError,e:
                #print str(e)
                pass




    #for row in matrix:
        #print row
    return matrix


def find_avg_outdegree():
    """

    Find the average outdegree of aoi_comm_new.csv file which indicates 
    which areas/projects of intrest have maximun potential for load balencing.
    It is also used to form a dictionary of area/project of intrest as keys and 
    the number of committees covering that area/project as the corresponding values.

    :rtype: Tuple
    :return: A tuple with the dictionary as first element and 
             average outdegree as other element.

    """
    
    out_degree = 0
    total_committees = 0
    aoe_comm_dict = {}
    _sum = 0
    with open('aoi_comm_new.csv','r') as f:
        output = csv.reader(f,delimiter = ' ')
        for row in output:
            aoe_comm_dict[row[0]] = int(len(row[1:]))

    for i in aoe_comm_dict.values():
        _sum += i
    avg_outdegree = _sum/len(aoe_comm_dict)
    return (aoe_comm_dict,avg_outdegree)
    #print aoe_comm_dict,avg_outdegree,len(aoe_comm_dict)



def segregate_edges():

    """

    Finds which edges can be used to achieve more amount of load balencing. This is 
    used to assign more weights to those edges with more potential to do load balencing. 
    Segregation is based on outdegree of the area of intrest which 
    are given as student preferances.

    :rtype: Tuple
    :return: A tuple with all preferances of students divided in two lists. 
             These two lists form the tuple.

    """

    aoe_comm_dict,avg_outdegree = find_avg_outdegree()
    list_alpha = []
    list_one_minus_alpha = []
    with open('final_stud_file.csv','r') as f:
        output = csv.reader(f,delimiter = ',')
        for row in output:
            for num in row[1:]:
                try:
                    if aoe_comm_dict[num]>avg_outdegree:
                        list_one_minus_alpha.append((row[0],num))
                    else:
                        list_alpha.append((row[0],num))
                except KeyError,e:
                    #print str(e)
		    pass
                    #pass
    #print list_alpha
    #print list_alpha
    print '\n'
    #print list_one_minus_alpha
    return (list_alpha,list_one_minus_alpha)
    #print list_one_minus_alpha


def find_aoe_comm_index(aoe_comm_list,elem):
    """
    Used to find the index of a specific area/project of intrest in the list of lists 
    of area/project of intrest and committees file.

    :rtype: Integer
    :return: The index of area/project of intrest in given list of lists.

    """

    for i,lst in enumerate(aoe_comm_list):
        if elem == lst[0]:
            return i


def make_matrix():
    #some_name(alpha,max_count,gamma)
    #find_avg_outdegree()
    #segregate_edges()
    create_stud_database()


if __name__ == '__main__':
    #some_name(sys.argv[1],sys.argv[2],sys.argv[3])
    make_matrix()
    #get_stud_row()
    #get_aoe_comm_list()
