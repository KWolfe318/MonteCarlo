class MonteCarlo:
    '''
    A class object that returns Monte Carlo simulations in a pandas dataframe.
    Arguments:
    start
    '''
  def __init__(self,start,steps,frequency,mu,vol,iter,jump_vol,lam):
    self.start = start
    self.steps = steps
    self.freq = self.Freq(frequency)
    self.mu = mu / self.freq
    self.vol = vol
    self.iter = iter
    self.jump_vol = jump_vol
    self.lam = lam
    self.gbm_gaussians = np.random.normal(loc=0,scale=1,size=[self.steps,self.iter])
    self.gbm_levels = self.GBM()
    self.merton_levels = self.merton()
    self.returns = pd.DataFrame(np.diff(np.log(self.gbm_levels)))
  
  def Freq(self,freq):
    dict = {'d':252,'w':52,'m':12,'y':1}
    try:
      return dict[freq.lower()]
    except:
      return Warning(Bad_Input,f"Must pass common timeframe abbreviation as string (d,w,m,y), received {type(freq).__name__} ({freq})")
  
  def GBM(self):
    trend_array = np.full([self.steps,self.iter],self.mu - ((self.vol**2)/2)*(1/self.freq))
    shock_array = np.full([self.steps,self.iter],self.vol*np.sqrt(1/self.freq)) * self.gbm_gaussians
    df = pd.DataFrame(np.full([1,self.iter],self.start)).append(pd.DataFrame(np.exp(trend_array + shock_array)).cumprod()*self.start,ignore_index=True)
    return df

  def merton(self):
    trend_array = np.full([self.steps,self.iter],self.mu - ((self.vol**2)/2)*(1/self.freq))
    shock_array = np.full([self.steps,self.iter],self.vol*np.sqrt(1/self.freq)) * self.gbm_gaussians
    jump_array = np.random.poisson(self.lam/self.freq,[self.steps,self.iter]) * np.random.normal(loc=0,scale=self.jump_vol,size=[self.steps,self.iter]) #Need to double check a "cumsum" that is in some sources.
    df = pd.DataFrame(np.full([1,self.iter],self.start)).append(pd.DataFrame(np.exp(trend_array + shock_array + jump_array)).cumprod()*self.start,ignore_index=True)
    return df
  

class Bad_Input:
  pass
