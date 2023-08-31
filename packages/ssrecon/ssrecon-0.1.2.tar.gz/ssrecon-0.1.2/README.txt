This is just a simple library to perform the subset sum process for negative and postive floats with integer keys. 


It loops through the potential number of combinations to match, starting with 1 and ending with the value you give it in the provide

ssrecon.find_match(<List of tuples (FLOAT, INT)>,<Target to match FLOAT>,<Number of combos to iterate to INT>,<Verbose BOOL>)

Example:
>>> a, b = ssrecon.find_match([(1.0,1),(2.0,2),(3.0,3)],4.0,3,True)
Attempting with 1 combos
Attempting with 2 combos
>>> a
[1, 3]
>>> b
[1.0, 3.0]