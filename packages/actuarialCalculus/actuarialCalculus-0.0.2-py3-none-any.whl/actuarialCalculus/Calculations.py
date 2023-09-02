import numpy as np

class Insurance:

  class Continuous:

    class Dum:
      def __init__(self,MaxAge, Age, Delta):
        self.MaxAge = MaxAge
        self.Age= Age
        self.Delta = Delta

      def Temporary(self,n):
        return (1-np.exp(-self.Delta*n))/(self.Delta*(self.MaxAge-self.Age))

      def Life(self):
        if self.Age > self.MaxAge:
          return 0
        return (1-np.exp(-self.Delta*(self.MaxAge-self.Age)))/(self.Delta*(self.MaxAge-self.Age))

      def PureDotal(self,n):
        return (np.exp(-self.Delta*n)*(self.MaxAge-self.Age-n))/(self.MaxAge-self.Age)

      def MixedDotal(self,n):
        return self.Temporary(n)+self.PureDotal(n)

    class Exponential:
      def __init__(self, Delta, Mu):
        self.Delta = Delta
        self.Mu = Mu

      def Temporary(self,n):
        return (self.Mu*(1-np.exp(-n*(self.Mu+self.Delta))))/(self.Mu+self.Delta)

      def Life(self):
        return self.Mu/(self.Mu+self.Delta)

      def PureDotal(self,n):
        return np.exp(-n*(self.Mu*self.Delta))

      def MixedDotal(self,n):
        return self.Temporary(n)+self.PureDotal(n)

  class Discrete:
    def __init__(self,LifeTable, Interest):
      self.LifeTable = LifeTable
      self.Interest = Interest
    def Life(self,w,x):
      sum =0
      for i in range(w-x):
        sum= sum+ (1+self.Interest)**(-(i+1))*LifeTables(self.LifeTable).NPX(x,i)*LifeTables(self.LifeTable).QX(x+i)
      return sum
    
    def Temporary(self,x,n):
      sum=0
      for i in range(n):
        sum = sum+ (1+self.Interest)**(-(i+1))*LifeTables(self.LifeTable).NPX(x,i)*LifeTables(self.LifeTable).QX(x+i)
      return sum

    def PureDotal(self,x,n):
      return LifeTables(self.LifeTable).NPX(x,n)*(1+self.Interest)**(-n)
    
    def MixedDotal(self,x,n):
      return self.Temporary(x,n)+self.PureDotal(x,n)
    


class Anuities:
  class Continuous:
    class Dum:
      def __init__(self,MaxAge,Age,Delta):
        self.MaxAge=MaxAge
        self.Age = Age
        self.Delta = Delta

      def Temporary(self,n):
        Dumx = Insurance().Continuous().Dum(self.MaxAge,self.Age,self.Delta)
        return (1-(Dumx.Temporary(n)+Dumx.PureDotal(n)))/self.Delta

      def Life(self):
        return (1-Insurance().Continuous().Dum(self.MaxAge,self.Age,self.Delta).Life())/self.Delta

    class Exponential:
      def __init__(self,Delta,Mu):
        self.Mu = Mu
        self.Delta = Delta

      def Temporary(self,n):
        return (1-np.exp(-n*(self.Mu+self.Delta)))/(self.Mu+self.Delta)

      def Life(self):
        return 1/(self.Mu+self.Delta)

  class Discrete:
    def __init__(self,LifeTable,Interest):
      self.LifeTable = LifeTable
      self.Interest = Interest

    def Life(self,w,x):
      return (1-Insurance.Discrete(self.LifeTable,self.Interest).Life(w,x))/(self.Interest/(1+self.Interest))

    def Temporary(self,x,n):
      return(1-Insurance.Discrete(self.LifeTable,self.Interest).MixedDotal(x,n))/(self.Interest/(1+self.Interest))
    
class LifeTables:
  def __init__(self, LifeTable):
    self.LifeTable = LifeTable

  def LX(self,x):
    lox = float(self.LifeTable.query(f"x=={x}")["lx"])
    if(lox is None):
      raise Exception(f"LX was not found for x={x}")
    return lox

  def DX(self,x):
    return self.LX(x)-self.LX(x+1)

  def NDX(self,x,n):
    return self.LX(x)-self.LX(x+n)

  def PX(self,x):
    return self.LX(x+1)/self.LX(x)

  def NPX(self,x,n):
    return self.LX(x+n)/self.LX(x)


  def QX(self,x):
    return self.DX(x)/self.LX(x)

  def NQX(self,x,n):
    return self.NDX(x,n)/self.LX(x)
  
  def MNQX(self,x,m,n):
    return self.NPX(x,m)*self.NQX(x+m,n)


class Premium:

  class Continuous:

    class Dum:
      def __init__(self,MaxAge,Age,Delta):
        self.MaxAge=MaxAge
        self.Age = Age
        self.Delta = Delta
      def Temporary(self,n):
        return Insurance.Continuous.Dum(self.MaxAge,self.Age,self.Delta).Temporary(n)/Anuities().Continuous().Dum(self.MaxAge,self.Age,self.Delta).Temporary(n)

      def Life(self):
        return Insurance.Continuous.Dum(self.MaxAge,self.Age,self.Delta).Life()/Anuities.Continuous.Dum(self.MaxAge,self.Age,self.Delta).Life()

      def PureDotal(self,n):
        return Insurance.Continuous.Dum(self.MaxAge,self.Age,self.Delta).PureDotal(n)/Anuities.Continuous.Dum(self.MaxAge,self.Age,self.Delta).Temporary(n)
      
      def MixedDotal(self,n):
        return Insurance.Continuous.Dum(self.MaxAge,self.Age,self.Delta).MixedDotal(n)/Anuities.Continuous.Dum(self.MaxAge,self.Age,self.Delta).Temporary(n)

    class Exponential:
      def __init__(self,Delta, Mu):
        self.Delta = Delta
        self.Mu = Mu

      def Temporary(self,n):
        return Insurance.Continuous.Exponential(self.Delta,self.Mu).Temporary(n)/Anuities().Continuous().Exponential(self.Delta,self.Mu).Temporary(n)

      def Life(self):
        return Insurance.Continuous.Exponential(self.Delta, self.Mu).Life()/Anuities.Continuous.Exponential(self.Delta, self.Mu).Life()

      def PureDotal(self,n):
        return Insurance.Continuous.Exponential(self.Delta, self.Mu).PureDotal(n)/Anuities.Continuous.Exponential(self.Delta,self.Mu).Temporary(n)

      def MixedDotal(self,n):
        return Insurance.Continuous.Exponential(self.Delta,self.Mu).MixedDotal(n)/Anuities.Continuous.Exponential(self.Delta, self.Mu).Temporary(n)


class Reserve:
  class Continuous:
    class Dum:
      def __init__(self,MaxAge, Age, Delta,InsuredSum):
        self.Age = Age
        self.Delta = Delta
        self.MaxAge = MaxAge
        self.InsuredSum = InsuredSum

      def Temporary(self,n,t):
        return self.InsuredSum*(Insurance().Continuous().Dum(self.MaxAge,self.Age+t,self.Delta).Temporary(n-t)-Premium().Continuous().Dum(self.MaxAge,self.Age,self.Delta).Temporary(n)*Anuities().Continuous().Dum(self.MaxAge,self.Age+t,self.Delta).Temporary(n-t))

      def Life(self,t):
        return self.InsuredSum*(Insurance.Continuous.Dum(self.MaxAge,self.Age+t,self.Delta).Life()-Premium.Continuous.Dum(self.MaxAge,self.Age,self.Delta).Life()*Anuities.Continuous.Dum(self.MaxAge,self.Age+t,self.Delta).Life())

      def PureDotal(self,n,t):
        return self.InsuredSum*(Insurance.Continuous.Dum(self.MaxAge,self.Age+t,self.Delta).PureDotal(n-t)-Premium.Continuous.Dum(self.MaxAge,self.Age,self.Delta).PureDotal(n)*Anuities.Continuous.Dum(self.MaxAge,self.Age+t,self.Delta).Temporary(n-t))
