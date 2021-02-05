# import argparse

# parser = argparse.ArgumentParser(description='Change the option prefix characters',
#                                  prefix_chars='-+/',
#                                  )

# parser.add_argument('-a', action="store_false", default=None,
#                     help='Turn A off',
#                     )
# parser.add_argument('+a', action="store_true", default=None,
#                     help='Turn A on',
#                     )
# parser.add_argument('//noarg', '++noarg', action="store_true", default=False)

# args = parser.parse_args()
# print(args)
# print(type(args))

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-db', "--database", help='an integer for the accumulator',
                    action="store_true")


args = parser.parse_args()

if args.database:
  print("got db")