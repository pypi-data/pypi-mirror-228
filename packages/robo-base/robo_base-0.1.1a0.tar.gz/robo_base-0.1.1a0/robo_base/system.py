## other promordal classes

from object import Object

class System(Object):
    # basically so far
    # common shell commands on
    # underlying OS/HW system
    # not the robots internal os/shell

   # def __init__(self):
    def __init__(self): #v0.07
    
       # super(Sensor, self).__init__()
        super(System, self).__init__()
         
        self._name = "SystemShell"
        self._desc = "OS/HW System shell functions"
        self._vers = "v0.01.01"  
        self._model = ""
        
    def kernelVersion(self):
        # not a get, not return string
        os.system('uname -r')
    
    def kernelVers(self):
        self.kernelVersion()
        
    def distroVersion(self):
        os.system('lsb_release -a')
    
    def distroVers(self):
        return self.distroVersion()
    
    def kernel(self):
        return self.kernelVers()
    
    def distro(self):
        return self.distroVers()
    
    def command(self,cmd):
        return os.system(cmd)
    
    def cmd(self,cmd):
        return self.command(cmd)
    
