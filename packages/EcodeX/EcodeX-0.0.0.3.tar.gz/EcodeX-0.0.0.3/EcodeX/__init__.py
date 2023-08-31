from zlib import compress
from os import makedirs,remove,walk,rename
from os.path import isdir,join,isfile
from hashlib import md5
import zipfile
from shutil import rmtree

__version__ = "0.0.0.1"

def Delete(folder_path):
    if isfile(folder_path):
        remove(folder_path)
    elif isdir(folder_path):
        rmtree(folder_path)

def zipdir(path, ziph):
   for root, dirs, files in walk(path):
       for file in files:
           ziph.write(join(root, file))

def zip(folder_path,zip_path):
   with zipfile.ZipFile(zip_path, 'w') as zipObj:
       zipdir(folder_path, zipObj)

class Install():
    def pack(self,name,icon,bao,version,version2,install_requires,author,author_email,description):
        self.name = name
        if not isdir('./'+self.name):
            makedirs('./'+self.name)
        if not isdir('./dist'):
            makedirs('./dist')
        open('./'+self.name+'/ICON','wb').write(open(icon,'rb').read())
        s = str(name)+'&s&'+str(bao)
        open('./'+self.name+'/SETTING','w').write(s)
        v = str(version)+'&v&'+str(version2)
        open('./'+self.name+'/VERSION','w').write(v)
        open('./'+self.name+'/INSTALL','w').write(str(install_requires))
        a = str(author)+'&a&'+str(author_email)
        open('./'+self.name+'/AUTHOR','w').write(a)
        open('./'+self.name+'/DESCRIPTION','w').write(str(description))
        md5a = open(icon,'rb').read() + s.encode('utf-8') + v.encode('utf-8')
        md5a += str(install_requires).encode('utf-8') + a.encode('utf-8')
        md5a += str(description).encode('utf-8')
        open('./'+self.name+'/MD5','wb').write(md5(md5a).digest())
        self.file(self.name)
        self.install()
    def file(self,file):
        zip(file,'./'+self.name+'/'+self.name)
    def install(self):
        zip('./'+self.name,'./dist/'+self.name+'1.sif')
        zip1 = open('./dist/'+self.name+'1.sif','rb').read()
        open('./dist/'+self.name+'.sif','wb').write(compress(zip1))
        remove('./dist/'+self.name+'1.sif')
        Delete(self.name)