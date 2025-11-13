from data_structures.object import Object, PreconditionObject
from unified_planning.model.fnode import FNode
import re

class Atom:
    def __init__(self, name, value,fluent,objects):
        self.name = name
        self.value = value
        self.objects = objects
        self.fluent = fluent
        

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash((self.name, self.value))

    def __repr__(self):
        return f"{self.name}={self.value}"
    
    

        
    def convertToGoalAtom(self):
        return GoalAtom(self.name,self.fluent,self.objects)
    
class GoalAtom:
    def __init__(self, name,fluent,objects):
        self.name = name
        self.objects = objects
        self.fluent = fluent
        
    def addObjectEncoding(self,encoding):
        newObjects = list()
        for i in self.objects:
            newObjects.append(PreconditionObject(i.name,i.type,encoding[i.name]))
        self.objects = newObjects
    
def extractAtom(key,value):
    objects = list()
    for obj in key.args:
        objects.append(Object(str(obj),obj.type.name))
    fluent = str(key).split("(")[0]
    return Atom(str(key),value,fluent,objects)

def extractGoalAtom(atom):
    objects = list()
    for obj in atom.args:
        objects.append(Object(str(obj),obj.type.name))
    fluent = str(atom).split("(")[0]
    return GoalAtom(str(atom),fluent,objects)


class PreconditionAtom:
    def __init__(self, name,fluent,objects):
        self.name = name
        self.objects = objects
        self.fluent = fluent
    
    def changeObjectName(self,newName):
        if len(self.objects) > 0:
            toChange = self.name.split("(")[1]
            for i in self.objects:
                if i.name in newName:
                    pattern = rf'(?<!_)({re.escape(i.name)})'
                    toChange = re.sub(pattern, newName[i.name], toChange)
                    #self.name = self.name.replace(i.name,newName[i.name])
                    i.name = newName[i.name]
            self.name = self.name.split("(")[0] + "(" + toChange
                
    def addObjectEncoding(self,encoding):
        newObjects = list()
        for i in self.objects:
            newObjects.append(PreconditionObject(i.name,i.type,encoding[i.name]))
        self.objects = newObjects
            
def extractPreconditionAtom(atom):
    objects = list()
    for obj in atom.args:
        objects.append(Object(str(obj),obj.type.name))
    fluent = str(atom).split("(")[0]

    return PreconditionAtom(str(atom),fluent,objects)

def extractPreconditionGnnAtom(atom):
    objects = list()
    for obj in atom.args:
        objects.append(Object(str(obj),obj.type.name))
    if isinstance(atom,FNode):
        fluent = str(atom).split("(")[0]
        return PreconditionAtom(str(atom),fluent,objects)
    else:
        fluent = atom.name.split("(")[0]
        return PreconditionAtom(atom.name,fluent,objects)

class EffectAtom:
    def __init__(self, name,fluent,objects):
        self.name = name
        self.objects = objects
        self.fluent = fluent
        
def extractEffectAtom(atom):
    objects = list()
    for obj in atom.args:
        objects.append(Object(str(obj),obj.type.name))
    fluent = str(atom).split("(")[0]
    return EffectAtom(str(atom),fluent,objects)