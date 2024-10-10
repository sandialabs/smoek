clean:
	\rm -f nlfiles/*.nl lpfiles/*lp models/*.cpp models/[a-z]*.py

pymodel:
	nohup time python test_pymodel.py 2>&1 > pymodel.out &

code:
	nohup time python test_code.py 2>&1 > code.out &
