# 2 = 1102
# 3 = 1301
# 4 = 1101
# 5 = 2102
# 6 = 2305

mkdir dump

python main.py inb1102 2
python main.py inb1301 3
python main.py inb1101 4
python main.py inb2102 5
python main.py inb2305 6

cat dump/inb*.sql > dump/big.sql