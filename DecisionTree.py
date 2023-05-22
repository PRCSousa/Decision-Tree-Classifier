import pandas as pd #for manipulating the csv data
import numpy as np #for mathematical calculation
import sys
import math
import copy

from Dataframe import *

def calc_total_entropy(train_data: DataFrame, label, class_list):
    ## print("\nCALCULATE TOTAL ENTROPY: ")
    ## print(" ")
    total_row = train_data.numEntradas #the total size of the dataset
    total_entr = 0
    
    for c in class_list: #for each class in the label
        ## print(c)
        total_class_count = 0
        total_class_count = len(train_data.if_contains(c)) #number of the class
        total_class_entr = 0
        total_class_entr = (float)(- (total_class_count/total_row)*np.log2(total_class_count/total_row)) #entropy of the class
        if math.isnan(total_class_entr):
            total_class_entr = 0
        ## print("Total Class Count:", total_class_count)
        ## print("Total Class Entropy:", total_class_entr)
        total_entr += total_class_entr #adding the class entropy to the total entropy of the dataset
    
    ## print("Total Entropy: ")
    ## print(total_entr)
    return total_entr

def calc_entropy(feature_value_list: list, feature_value_data: DataFrame, label, class_list) -> float:

    '''
    Calculates the entropy of the feature value

    Parameters
    ----------------
    - feature_value_data : List  of the feature values
    - label : label of the dataset (target column)
    - class_list : list of the classes in the label
    '''
    ## print("\nCALCULATE ENTROPY OF ATRIBUTE: ")
    ## feature_value_data.print_csv()
    ## print(label)
    ## print(class_list)

    class_count = feature_value_data.numEntradas
    entropy = 0
    
    for c in class_list:
        label_class_count = len(feature_value_data.if_contains(c))#row count of class c 
        ## print("\n Count de entradas com label " + c + ": ")
        ## print(label_class_count)
        ## print(feature_value_data.if_contains(c))
        
        entropy_class = 0

        if label_class_count != 0:
            probability_class = label_class_count/class_count #probability of the class
            entropy_class = - probability_class * np.log2(probability_class)  #entropy
        entropy += entropy_class

    return entropy

def calc_info_gain(feature_name, train_data: DataFrame, label: int, class_list: list):

    ## print("\nCALC INFO GAIN: ")
    ## print("Feature Name:" + feature_name)
    ## print("Train Data: ")
    ## train_data.print_csv()
    ## print("Label: " + label)
    ## print("Class List: ")
    ## print(class_list)

    feature_value_list = train_data.get_unique_values(train_data.getColumn(feature_name)) #unqiue values of the feature

    ## print("Feature Value List")
    ## print(feature_value_list)

    total_row = train_data.numEntradas
    feature_info = 0.0
    
    for feature_value in feature_value_list:
        feature_value_data = train_data.if_contains(feature_value) #filtering rows with that feature_value
        feature_value_data.insert(0, train_data.atributos)
        feature_value_data = DataFrame("nan", matrix= feature_value_data)
        ## print("Train Data que contém " + feature_value + ":")
        ## print(feature_value_data.print_csv())

        feature_value_count = feature_value_data.numEntradas
        feature_value_entropy = calc_entropy(feature_value_list, feature_value_data, label, class_list) #calculcating entropy for the feature value
        feature_value_probability = feature_value_count/total_row
        feature_info += feature_value_probability * feature_value_entropy #calculating information of the feature value
        ## print("Feature value: ", feature_value)
        ## print("Feature info gain: ", feature_info)
        
    return calc_total_entropy(train_data, label, class_list) - feature_info #calculating information gain by subtracting


def find_most_informative_feature(train_data: DataFrame, label: str, class_list: list):
    ## print("FIND MOST INFORMATIVE FEATURE: ")
    ## print(" ")
    feature_list = train_data.atributos #finding the feature names in the dataset
    max_info_gain = -1
    max_info_feature = None
    
    for feature in feature_list[:-1]:  #for each feature in the dataset
        feature_info_gain = calc_info_gain(feature, train_data, label, class_list)
        ## print("VALOR DE " + feature + ": ")
        ## print(feature_info_gain)
        if max_info_gain < feature_info_gain: #selecting feature name with highest information gain
            max_info_gain = feature_info_gain
            max_info_feature = feature
    
    ## print("Max info gain: ", max_info_feature)
    return max_info_feature


def make_tree(root: dict, train_data: DataFrame, label: str, class_list: list):
    ## print("MAKE TREE: ")
    ## print("train data on this node: ")
    ## train_data.print_csv()
    ## print(" ")

    if len(train_data.get_data()) != 0: #if dataset becomes enpty after updating

        # if all the rows have same class
        if len(train_data.get_unique_values(train_data.getColumn(label))) == 1:
            ## print("All rows have same class")
            root = train_data.get_unique_values(train_data.getColumn(label))[0]
            return root

        # if there are no more features
        if len(train_data.atributos) == 1:
            ## print("No more features")
            root = train_data.get_unique_values(train_data.getColumn(label))[0]
            return root

        max_info_feature = find_most_informative_feature(train_data, label, class_list) #most informative feature    

        ## print("BEGINNING THE TREE MAKING PROCESS:")
        ## print("Max info feature: ", max_info_feature)

        # separate the dataset based on the most informative feature and make subtrees based on the values of the feature

        feature_value_list = train_data.get_unique_values(train_data.getColumn(max_info_feature)) #unqiue values of the feature
        ## print("Feature value list: ", feature_value_list)
        tree= {} #root of the tree
        col = train_data.getColumn(max_info_feature)
        for feature_value in feature_value_list:
            node = [] # gonna save the attribute name, entry count and further dictionaries
            node.append(max_info_feature)
            ## print("Feature value: ", feature_value)
            ## print("Train data before subdividing it: ")
            ## train_data.print_csv()
            # reset subdata
            sub_data = []
            sub_data = copy.deepcopy(train_data.if_contains_in_column(feature_value, col)) #filtering rows with that feature_value
            ## print("Subdata: ")
            ## print(sub_data)
            # converting the list to dataframe and dropping the max feature column
            # make deepcopies before passing to the function to avoid changing the original dataset

            atributos = copy.deepcopy(train_data.atributos)
            sub_data.insert(0, atributos)
            sub_data = DataFrame("nan", matrix= sub_data)
            ## print("Subdata before dropping featured column")
            ## sub_data.print_csv()
            sub_data.drop(col) #dropping the feature column
            ## print("Subdata after dropping featured column")
            ## sub_data.print_csv()
            node.append(sub_data.numEntradas)
            # if there are no more entries
            if len(sub_data.get_data()) == 0:
                ## print("No more entries")
                # define the leaf node as the most common class
                root[max_info_feature][feature_value] = train_data.get_most_common_class(train_data.getColumn(label))
                return tree
            
            tree.update({feature_value: {}}) #updating the tree with the feature name

            # recursive call to make_tree
            sub_dict = make_tree(tree[feature_value], sub_data, label, class_list)
            node.append(sub_dict)
            tree[feature_value] = node #updating the tree with the subtree

    return tree

def print_dictionary(dictionary, indent=''):
    for key, value in dictionary.items():
        attribute, count, sub_dict = value

        print(indent + attribute + ":")
        print(indent + '    ' + key + ': ', end= '')
        
        if isinstance(sub_dict, str):
            print(sub_dict + " (" + str(count) + ")")
        else:
            print("")
            print_dictionary(sub_dict, indent + "    ")

# lero print

def id3(train_data: DataFrame, TarCol: int) -> dict:
    tree = {} #tree which will be updated
    class_list = train_data.get_unique_values(TarCol) #getting unqiue classes of the label
    # DEBUG
    ## print(class_list)
    label = train_data.atributos[TarCol] #getting the label name
    return make_tree(tree, train_data, label, class_list) #start calling recursion


df = DataFrame("datasets/" + sys.argv[1] + ".csv") #importing the dataset from the disk
df.read_csv() #reading the dataset
df.drop(0) # drop the ID row
df.format_continuous()

tree = id3(df, df.targetCol)

print_dictionary(tree)
