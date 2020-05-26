### Provided for informational purposes only.

## How to get keys

Requirements: Android with ROOT-rights.

`/data/data/app.source.getcontact/shared_prefs/GetContactSettingsPref.xml` 

## How to run 

Install [tesseract](https://github.com/tesseract-ocr/tesseract/wiki)

Install all dependencies from requirements.txt

```shell script
pip3 install -r requirements.txt
```

## Run

**Result stores in `get_contact.xls`**

You can restore last session with `-r` flag.
The program will find the last number in the xls file and skip all the numbers that go before it.

You can also disable output using `-v 0`

```shell script
usage: /home/mrgyber/PycharmProjects/getcontact/getcontact.py [options] -f file
       [-h] [-f FILE] [-s SEP] [-r] [-v VERBOSE]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File with number intervals
  -s SEP, --sep SEP     Separator for number intervals (space by default)
  -r, --restore         Restores the previous session
  -v VERBOSE, --verbose VERBOSE
                        0 = no output; 1 = everything except the captcha; 2 =
                        everything (1 by default)
```

Input:
```shell script
python3 getcontact.py -f phones_example.txt -s -
```

Output example:
```text
...
[FOUND] 	 +89297000132: ['Олег Ермолаев', 'Олег Николаевич', 'Олег Ермолаев Менеджер', 'Олег Ермолаев Мегафон', 'Олег Мегафон Мичурина', 'B-oleg Ermolaev Aetp', 'Олег Еримеев Мегафон', 'Ново Вокзальная', 'Олег Гарант', 'Dodge']
[EMPTY] 	 +89297000133
[EMPTY] 	 +89297000139
[EMPTY] 	 +89297000130
[FOUND] 	 +89297000141: ['Синицын Александр Терм.оборуд.', 'Александр Синицын Мегафон', 'Александр Синицин', 'Александр Синицын', 'Александр Вячеславович Синицын', 'Александр Мегафон', 'Синицин Александр', 'Продажа Sedge', 'Синицын Саша', 'Р Синицын', 'Синицин']
[EMPTY] 	 +89297000149
[EMPTY] 	 +89297000137
[FOUND] 	 +89297000150: ['Руслан Байтаков Самгту', 'Байдаков Руслан Рашидович Налоговая', 'Руслан Байдаков', 'Руслан']
[EMPTY] 	 +89297000138
[EMPTY] 	 +89297000151
...
```
