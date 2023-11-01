class Phone():
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def callMe(self):
    print(self.x,self.y)


natalie = Phone(2,3)
natalie.callMe()

ls = [5,5]
chloe = Phone(5,5)
chloe.callMe()