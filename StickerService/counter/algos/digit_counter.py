def count_numbers_with_digit(digit, n):
    # Since we know that each number can appear only once in the set 0-9, we can use that
    # calculate each rollover of 10, and remove the digits that were already counted.

    # For example, we know that in 100, there are ten 10s, because 100/10 = 10, so we can say that
    # cur = 100, prev = 10, and we know there must be a 7 in each of those, so (100/10) * 1 or using
    # variables (cur/prev) * lookup[prev], where the lookup are known values (i.e. a single 7).
    # Next, we need to account for 7 in other positions, such as in the 70s where 7 appears each time.
    # That is trivial, we know that 7 appears 10 times in the tens column, so we can add that to our
    # current total for 100. However, we keep in mind that we already counted a 7 when counting the 10s.
    # Therefore, we need to subtract however many 7s are in a set of 10, which we can do by checking
    # the previous lookup, and the final we add is (prev - lookup[prev]).
    lookup = {1: 0, 10: 1}
    cur = 1
    for i in range(len(str(n))):
        prev = cur
        cur *= 10
        lookup[cur] = ((cur / prev) * lookup[prev]) + (prev - lookup[prev])

    # Originally, I had attempted to solve the problem in a more complex way, keeping track of previous
    # remainders, and so on. However, while working on the problem I realized in my own head I was doing a
    # simple breakdown of finding the first 7, and adding everything after that digit. I decided to
    # do that and simplify the problem. If the digit is first seen in the ones column, we add 1.
    asi = 0
    if str(digit) in str(n):
        asi = int(str(n)[str(n).index(str(digit))+1:] or 1)
        n -= asi

    count = 0
    position = 1

    while n > 0:

        quotient = n // 10  # get the numbers to the left
        remainder = n % 10  # get the far right number

        count += remainder * lookup[position]  # use the lookup table to know how many for this column

        if remainder > digit:  # if we are above the digit
            count += position  # add whatever power of 10 our current column
            count -= lookup[position]  # subtract whatever we already added in {remainder * lookup[position]}

        if remainder == digit:  # if we are on that exact digit
            count += 1  # add a humble one

        n = quotient  # take the numbers that were on the left
        position *= 10  # move up in column value

    # since we are counting from 1 to n
    if digit == 0:
        count -= 1

    return round(count + asi)
