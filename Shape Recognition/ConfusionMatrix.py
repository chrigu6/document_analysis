'''
Created on Mar 2, 2015

@author: chrigu
'''

class ConfusionMatrix:
    
    def __init__(self):
        self.categories = []

    def addResult(self,pair):
        if not self.contains(pair[0]):
            self.categories.append([pair[0],[pair[1]]])
        
        else: 
            for element in self.categories:
                if element[0] == pair[0]:
                    element[1].append(pair[1])
        
    
    def contains(self, name):
        for element in self.categories:
            if element[0] == name:
                return True
        return False
    
    def getCategories(self):
        result = ""
        for element in self.categories:
            result = result + element[0] + "\t".expandtabs(12-len(element[0]))
        return result
                
    def matches(self, results, figure):
        matches = 0.0
        for element in results:
            if element == figure:
                matches = matches + 1.0
                
        return round((matches/len(results)),3)
        
    
    def __str__(self):
        result = "\t".expandtabs(12) + self. getCategories() + "\n"
        
        for element in self.categories:
            result = result + element[0] + "\t".expandtabs(12-len(element[0])) 
            for element2 in self.categories:
                result = result + '%4.3F'%self.matches(element[1],element2[0]) + "\t".expandtabs(7)
            result = result + "\n"
        return result
                
                
            
        
                        


