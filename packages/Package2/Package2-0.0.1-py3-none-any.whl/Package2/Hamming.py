# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 17:33:09 2023

@author: ANASUA
"""
class Hamming:
    def __init__(self,string1,string2):
        self.string1 = string1
        self.string2 = string2
    

    def hamming_distance(self): ## input: string1 and string2 of same length
         
        if len(self.string1) != len(self.string2):
            raise ValueError("Input strings must have the same length")
            
        else:
            
            distance = 0  # Start with a distance of zero
    
            L = len(self.string1)  ## length of the strings
            for i in range(L): # Loop over the indices of the string
        
               if self.string1[i] != self.string2[i]:   ## if the two characters of same indices are not equal
                    distance = distance + (2**(L-(i+1)))

        return distance ## Return the Hamming distance between string1 and string2, i.e. the 

