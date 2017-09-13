from s2m.core.parser import Token

def reduce_1(name, d, f):

    return lambda x, name=name, d=d, f=f: (Token(name, [f(d[x])]) if x in d.keys() else None)

def reduce_2(name, i, word):
    
    return lambda x,name=name,i=i,word=word: (Token(name + '.' + str(i)) if x==word else None)

def _1_ff(name):

    return lambda x,y,name=name: (Token(name + '.0t1', x.formula + y.formula)
                                  if x.is_full_formula and y.is_full_formula
                                  else None)

def _1_ft(name, tag):
                                           
    return lambda x,y,name=name,tag=tag: (Token(name + '.0t1', x.formula + y.formula)
                                          if x.is_full_formula and y.tag == tag
                                          else None)

def _1_fw(name):

    return lambda x,y,name=name: (Token(name + '.0t1', x.formula)
                                  if x.is_full_formula and y.tag == name + '.1'
                                  else None)

def _1_tf(name, tag):

    return lambda x,y,name=name,tag=tag: (Token(name + '.0t1', x.formula + y.formula)
                                          if x.tag == tag and y.is_full_formula
                                          else None)

def _1_tt(name, tag1, tag2):
    
    return lambda x,y,name=name,tag1=tag1,tag2=tag2: (Token(name + '.0t1', x.formula + y.formula)
                                                      if x.tag == tag1 and y.tag == tag2
                                                      else None)

def _1_tw(name, tag):

    return lambda x,y,name=name,tag=tag: (Token(name + '.0t1', x.formula)
                                          if x.tag == tag and y.tag == name + '.1'
                                          else None)

def _1_wf(name):

    return lambda x,y,name=name: (Token(name + '.0t1', y.formula)
                                  if x.tag == name + '.0' and y.is_full_formula
                                  else None)

def _1_wt(name, tag):

    return lambda x,y,name=name,tag=tag: (Token(name + '.0t1', y.formula)
                                          if x.tag == name + '.0' and y.tag == tag
                                          else None)

def _1_ww(name):

    return lambda x,y,name=name: (Token(name + '.0t1', [])
                                  if x.tag == name + '.0' and y.tag == name + '.1'
                                  else None)

def _2_ff(name, f):

    return lambda x,y,name=name,f=f: (Token(name, [f(x.formula + y.formula)])
                                      if x.is_full_formula and y.is_full_formula
                                      else None)

def _2_ft(name, tag, f):
                                           
    return lambda x,y,name=name,tag=tag,f=f: (Token(name, [f(x.formula + y.formula)])
                                              if x.is_full_formula and y.tag == tag
                                              else None)

def _2_fw(name, f):

    return lambda x,y,name=name,f=f: (Token(name, [f(x.formula)])
                                      if x.is_full_formula and y.tag == name + '.1'
                                      else None)

def _2_tf(name, tag, f):

    return lambda x,y,name=name,tag=tag,f=f: (Token(name, [f(x.formula + y.formula)])
                                              if x.tag == tag and y.is_full_formula
                                              else None)

def _2_tt(name, tag1, tag2, f):
    
    return lambda x,y,name=name,tag1=tag1,tag2=tag2,f=f: (Token(name, [f(x.formula + y.formula)])
                                                          if x.tag == tag1 and y.tag == tag2
                                                          else None)

def _2_tw(name, tag, f):

    return lambda x,y,name=name,tag=tag,f=f: (Token(name, [f(x.formula)])
                                              if x.tag == tag and y.tag == name + '.1'
                                              else None)

def _2_wf(name, f):

    return lambda x,y,name=name,f=f: (Token(name, [f(y.formula)])
                                      if x.tag == name + '.0' and y.is_full_formula
                                      else None)

def _2_wt(name, tag, f):

    return lambda x,y,name=name,tag=tag,f=f: (Token(name, [f(y.formula)])
                                              if x.tag == name + '.0' and y.tag == tag
                                              else None)

def _2_ww(name, f):

    return lambda x,y,name=name,f=f: (Token(name, [f([])])
                                      if x.tag == name + '.0' and y.tag == name + '.1'
                                      else None)

def i_f(name, i):

    return lambda x,y,name=name,i=i: (Token(name + '.0t' + str(i), x.formula + y.formula)
                                      if x.tag == name + '.0t' + str(i-1) and y.is_full_formula
                                      else None)

def i_t(name, i, tag):

    return lambda x,y,name=name,i=i,tag=tag: (Token(name + '.0t' + str(i), x.formula)
                                              if x.tag == name + '.0t' + str(i-1) and y.tag == tag
                                              else None)

def i_w(name, i):

    return lambda x,y,name=name,i=i: (Token(name + '.0t' + str(i), x.formula)
                                      if x.tag == name + '.0t' + str(i-1) and y.tag == name + '.' + str(i)
                                      else None)

def l_f(name, i, f):

    return lambda x,y,name=name,i=i,f=f: (Token(name, [f(x.formula + y.formula)])
                                                     if x.tag == name + '.0t' + str(i-1) and y.is_full_formula
                                                     else None)

def l_t(name, i, tag, f):

    return  lambda x,y,name=name,i=i,tag=tag,f=f: (Token(name, [f(x.formula + y.formula)])
                                                   if x.tag == name + '.0t' + str(i-1) and y.tag == tag
                                                   else None)

def l_w(name, i, f):

    return lambda x,y,name=name,i=i,f=f: (Token(name, [f(x.formula)])
                                          if x.tag == name + '.0t' + str(i-1) and y.tag == name + '.' + str(i)
                                          else None)
