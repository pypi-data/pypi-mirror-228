"""Console script for nlptools."""
import argparse
from nlptools.utils.parser import arStrip
import sys
"""
  This method removes Arabic diacritics, small diacritcs, shaddah, Latin and Arabic digits, and unify alif.
  And remove special characters, spaces, underscore and Arabic tatwelah from the input text.
  Args:
  text (:obj:`str`): Arabic text to be processed.
  diacs (:obj:`bool`): flag to remove Arabic diacretics [ ًٌٍَُِْ] (default is True).
  smallDiacs (:obj:`bool`): flag to remove small diacretics (default is True).
  shaddah (:obj:`bool`): flag to remove shaddah (default is True).
  digit (:obj:`bool`): flag to remove Latin and Arabic digits (default is True).
  alif (:obj:`bool`): flag to unify alif (default is True).
  specialChars (:obj:`bool`): flag to remove special characters (default is True). 
"""

def main():
    # """Console script for nlptools."""
    # parser = argparse.ArgumentParser()
    # parser.add_argument('_', nargs='*')
    # args = parser.parse_args()
# 
    # print("Arguments: " + str(args._))
    # print("Replace this message by putting your code into "
        #   "nlptools.cli.main")
    # return 0
    parser = argparse.ArgumentParser(description='Arabic text stripping tool using SinaTools')
    
    parser.add_argument('--text', type=str, required=True, help='Text to be stripped')
    parser.add_argument('--diacs', type=bool, default=True, help='Whether to strip diacritics')
    parser.add_argument('--smallDiacs', type=bool, default=True, help='Whether to strip small diacritics')
    parser.add_argument('--shaddah', type=bool, default=True, help='Whether to strip shaddah')
    parser.add_argument('--digit', type=bool, default=True, help='Whether to strip digits')
    parser.add_argument('--alif', type=bool, default=True, help='Whether to strip alif')
    parser.add_argument('--specialChars', type=bool, default=True, help='Whether to strip special characters')

    args = parser.parse_args()

    stripped_text = arStrip(args.text, diacs=args.diacs, smallDiacs=args.smallDiacs, 
                            shaddah=args.shaddah, digit=args.digit, alif=args.alif, specialChars=args.specialChars)
    
    print(stripped_text)    


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover