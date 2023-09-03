from hak.one.dict.is_a import f as is_dict
from hak.pf import f as pf
from hak.pxyf import f as pxyf

# misc.dict.keypaths.leaf.get
# make_b
def f(x, path_so_far=[], keypaths=set()):
  for k in x:
    keypaths |= (
      f(x[k], path_so_far+[k], keypaths)
      if is_dict(x[k]) else
      set([tuple(path_so_far+[k])])
    )
  return keypaths

def t_a():
  x = {
    'Name': 'Alice',
    'Info': {
      'Age': 28,
      'Country': 'USA',
      'Appearance': {'Eye Colour': 'Green', 'Height': 1.85}
    }
  }
  y = set([
    ('Name',),
    ('Info', 'Age'),
    ('Info', 'Country'),
    ('Info', 'Appearance', 'Eye Colour'),
    ('Info', 'Appearance', 'Height')
  ])
  return pxyf(x, y, f, new_line=1)

def t():
  if not t_a(): return pf('!t_a')
  return True
