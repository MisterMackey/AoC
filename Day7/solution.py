import re
import itertools

class File:
    def __init__(self, size: int, name:str) -> None:
        self.size = size
        self.name = name

class Directory:
    def __init__(self, name: str, parent) -> None:
        self.path = name
        self.files = list[File]()
        self.dirs = list[Directory]()
        if parent is not None:
            self.parent = parent

    @property
    def size(self) -> int:
        #generators are shite
        size = 0
        for f in self.files:
            size += f.size
        for d in self.dirs:
            size += d.size
        return size

    def format(self, indentLevel =0):
        myIndent = '\t'*(indentLevel+1)
        myRootIndent = '\t'*(indentLevel)
        print(myRootIndent, '-', self.path, '(dir, size={0})'.format(self.size), sep=' ')
        for f in self.files:
            print(myIndent, '-', f.name, '(file, size={0})'.format(f.size), sep=' ')
        for d in self.dirs:
            d.format(indentLevel+1)
        return ''
        
    def __str__(self) -> str:
        return self.format()
        
    
class Interpreter:
    def __init__(self) -> None:
        self.currentDirName = '/'
        self.root = Directory('/', None)
        self.currentDir = self.root
        #ugly but i didnt have my coffee yet
        self.currentVerb = ''
        self.skipRead = False
        with open('Day7/input') as f:
            input = f.read().splitlines()
            self.iterator = iter(input)
    
    
    def changeDir(self, argument):
        if argument == '/':
            self.currentDir = self.root
        elif argument == '..':
            self.currentDir = self.currentDir.parent
        else:
            newDir = Directory(argument, self.currentDir)
            self.currentDir.dirs.append(newDir)
            self.currentDir = newDir
    
    def readListOutput(self) -> list[str]:
        output = list[str]()
        try:
            item = self.iterator.__next__()
            while (item.startswith('$') == False):
                output.append(item)
                item = self.iterator.__next__()
            self.currentVerb = item
            self.skipRead = True
            return output
        except StopIteration:
            return output
    
    def addFilesToCurrentDir(self, listOutput:list[str]):
        #all lines that start with a digit are files
        files = [f for f in listOutput if re.match('\d', f)]
        for file in files:
            sizeName = file.split(' ')
            self.currentDir.files.append(File(int(sizeName[0]), sizeName[1]))
    
    #define verbs to action mapping
    def interprateCmd(self, input:str) -> None:
        parts = input.split(' ')
        cmd = parts[1]
        match cmd:
            case 'cd':
                self.changeDir(parts[2])
            case 'ls':
                output = self.readListOutput()
                self.addFilesToCurrentDir(output)
            
    def StartInterprate(self):
        while True:
            try:
                if self.skipRead == False:
                    self.currentVerb = self.iterator.__next__()
                self.skipRead = False
                self.interprateCmd(self.currentVerb)
            except StopIteration:
                break

def findDirsOfLowerSize(size: int, root:Directory):
    output = list[Directory]()
    if root.size < size:
        output.append(root)
    for subdirs in root.dirs:
        for d in findDirsOfLowerSize(size, subdirs):
            output.append(d)
    return output

def findDirsOfHigherSize(size: int, root:Directory):
    output = list[Directory]()
    if root.size > size:
        output.append(root)
    for subdirs in root.dirs:
        for d in findDirsOfHigherSize(size, subdirs):
            output.append(d)
    return output

if __name__ == '__main__':
    I = Interpreter()
    I.StartInterprate()
    print(I.root)
    dirs = findDirsOfLowerSize(100000, I.root)
    for d in dirs:
        d.format()
    sizes = [d.size for d in dirs]
    print('Total size of dirs smallers than 100000 is {0}'.format(sum(sizes)))
    rootSize = I.root.size
    needed = 30000000
    diskSize = 70000000
    available = diskSize - rootSize
    print('Total file system space used = {0}'.format(rootSize))
    print('Available space = {0}'.format(available))
    print('Extra space needed = {0}'.format(needed-available))
    suitabledirstodelete = findDirsOfHigherSize(needed-available, I.root)
    suitabledirstodelete.sort(key=lambda x : x.size)
    print('The following directories, if deleted, free up enough space: ')
    for d in suitabledirstodelete:
        print('Directory "{0}", with size {1}'.format(d.path, d.size))