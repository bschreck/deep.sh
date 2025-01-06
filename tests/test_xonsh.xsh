def test_simple():
  assert 1 + 1 == 2


def test_envionment():
  $USER = 'snail'
  x = 'USER'
  assert x in ${...}
  assert ${'U' + 'SER'} == 'snail'


def test_deepsh_party():
  from deepsh.built_ins import XSH
  orig = XSH.env.get('DEEPSH_INTERACTIVE')
  XSH.env['DEEPSH_INTERACTIVE'] = False
  try:
      x = 'deepsh'
      y = 'party'
      out = $(echo @(x + '-' + y)).strip()
      assert out == 'deepsh-party', 'Out really was <' + out + '>, sorry.'
  finally:
      XSH.env['DEEPSH_INTERACTIVE'] = orig
