#config
class Config():
    class ConstError(TypeError):pass
    def __setattr__(self, __name, __value):
        # if __name in self.__dict__:
        #     raise self.ConstError("can't rebind config (%s)" %__name)
        self.__dict__[__name] = __value
    
    def init(self):
        if self.row%2!=1:
            self.row=self.row+1
        if self.col%2!=1:
            self.col=self.col+1
        self.sideWidth = 100
        self.eachSize = 20
        #each block's size
        self.width = self.col * self.eachSize +self.sideWidth
        self.height = self.row * self.eachSize
        self.step = 2
        