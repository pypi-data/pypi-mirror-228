# ignore_overlength_lines

from datetime import date
from hak.one.rate.rate import Rate
from hak.one.table.table import Table
from hak.pxyz import f as pxyz

f = lambda x: str(Table().add_records(x))

def t():
  x = [
    {
      'date': date(2023, 1, 1),
      'cecil': {
        'robert': {'john': {'zenn': 0, 'rei': 1}, 'james': 'abcxyz'},
        'wendi': {'bec': {'theo': 3.14159, 'max': 3.149}},
        'liz': True,
        'donald': 6,
        'price': Rate(1, 2, {'$': 1, 'item': -1})
      }
    },
    {
      'date': date(2023, 1, 1),
      'cecil': {
        'robert': {'john': {'zenn': 7, 'rei': 8}, 'james': 'defuvw'},
        'wendi': {'bec': {'theo': 10, 'max': 11}},
        'liz': True,
        'donald': None,
        'price': Rate(2, 3, {'$': 1, 'item': -1})
      }
    },
    {
      'date': date(2023, 1, 1),
      'cecil': {
        'robert': {'john': {'zenn': 14, 'rei': 15}, 'james': 'ghipqrs'},
        'wendi': {'bec': {'theo': 17, 'max': 18}},
        'liz': False,
        'donald': 20,
        'price': Rate(4, 5, {'$': 1, 'item': -1})
      }
    }
  ]
  y = '\n'.join([
    '-------------------------------------------------------------------------',
    '                           cecil                            |    date    ',
    '------------------------------------------------------------|            ',
    ' donald | liz | price  |        robert        |    wendi    |            ',
    '        |     |        |----------------------|-------------|            ',
    '        |     |        |  james  |    john    |     bec     |            ',
    '        |     |        |         |------------|-------------|            ',
    '        |     |        |         | rei | zenn | max  | theo |            ',
    '--------|-----|--------|---------|-----|------|------|------|------------',
    '        |     | $/item |         |     |      |      |      |            ',
    '--------|-----|--------|---------|-----|------|------|------|------------',
    '      6 |   \x1b[1;32mY\x1b[0;0m |    1/2 |  abcxyz |   1 |      | 3.15 | 3.14 | 2023-01-01 ',
    '        |   \x1b[1;32mY\x1b[0;0m |    2/3 |  defuvw |   8 |    7 |   11 |   10 | 2023-01-01 ',
    '     20 |   \x1b[1;31mN\x1b[0;0m |    4/5 | ghipqrs |  15 |   14 |   18 |   17 | 2023-01-01 ',
    '--------|-----|--------|---------|-----|------|------|------|------------'
  ])

  z = f(x)
  return pxyz(x, y, z)

if __name__ == '__main__':
  result = t()
  print(int(result), end='')
