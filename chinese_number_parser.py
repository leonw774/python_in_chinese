import re
import typing

ch_num_table = {
	'零': 0,
	'一': 1,
	'二': 2,
	'三': 3,
	'四': 4,
	'五': 5,
	'六': 6,
	'七': 7,
	'八': 8,
	'九': 9,
	'十': 10,
	'百': 100,
	'千': 1000,
	'萬': 10000,
	'万': 10000,
	'億': 1_0000_0000,
	'亿': 1_0000_0000,
    '兆': 1_0000_0000_0000,
	'兩': 2,
	'两': 2,
	'〇': 0,
}

signs       = r'正負负\+-'
zeros       = r'零〇'
digits      = r'零〇一二兩两三四五六七八九'
dec_points  = r'點点\.'
small_units = r'十百千'
large_units = r'萬万億亿兆'

# < 1_0000
small_unit_int_pattern = \
    f'([{zeros}]?[{digits}]?[{small_units}])' + r'{0,3}' + f'[{digits}]?'
# >= 1_0000
big_unit_int_pattern = \
    f'(({small_unit_int_pattern})[{large_units}])*({small_unit_int_pattern})?'

decimal_pattern = r'[點点\.]' + f'[{digits}]+'
no_unit_pattern = f'^[{signs}]?[{digits}]+({decimal_pattern})?$'
unit_pattern    = f'^[{signs}]?{big_unit_int_pattern}({decimal_pattern})?$'

decimal_pattern = re.compile(decimal_pattern)
no_unit_pattern = re.compile(no_unit_pattern)
unit_pattern = re.compile(unit_pattern)

# print(decimal_pattern)
# print(no_unit_pattern)
# print(unit_pattern)

def parse_ch_num(test_str: str) -> typing.Union[str, int, float]:
    '''If success, return the int or float. If failed, return itself'''
    if re.match(r'$\s*^', test_str):
        # print('whites', [test_str])
        return test_str

    is_unit_number = None
    if no_unit_pattern.match(test_str):
        # print('has no unit', test_str)
        is_unit_number = False
    elif unit_pattern.match(test_str):
        # print('have unit', test_str)
        is_unit_number = True
    else:
        return test_str
    
    sign = 1
    if test_str[0] in '負负-':
        sign = -1
    if test_str[0] in signs:
        if len(test_str) == 1:
            return test_str
        else:
            test_str = test_str[1:]

    has_decimal = re.search(decimal_pattern, test_str)
    parsed_number = None

    try:
        if is_unit_number:
            large_unit_int = 0
            small_unit_int = 0
            coeff_int = 0
            for c in test_str:
                if c in digits:
                    assert coeff_int == 0
                    coeff_int = ch_num_table[c]

                elif c in small_units:
                    c_num = ch_num_table[c]
                    if c_num != 10:
                        assert coeff_int != 0
                    elif coeff_int == 0:
                        coeff_int = 1
                    assert (small_unit_int == 0 or 
                            small_unit_int > coeff_int * c_num)
                    small_unit_int += coeff_int * c_num
                    coeff_int = 0

                elif c in large_units:
                    c_num = ch_num_table[c]
                    if coeff_int != 0:
                        small_unit_int += coeff_int
                        coeff_int = 0
                    assert (large_unit_int == 0 or
                            large_unit_int > small_unit_int * c_num)
                    large_unit_int += small_unit_int * c_num
                    small_unit_int = 0

                elif c in dec_points:
                    break
                # print(large_unit_int, small_unit_int, coeff_int)

            if coeff_int != 0:
                smallest_nonzero_place = 1
                while (small_unit_int // 10) % smallest_nonzero_place == 0:
                    smallest_nonzero_place *= 10

                small_unit_int += int(coeff_int * (smallest_nonzero_place / 10))
            large_unit_int += small_unit_int
            
            parsed_number = large_unit_int

        elif not is_unit_number:
            parsed_number = 0
            for c in test_str:
                if c in dec_points:
                    break
                parsed_number = parsed_number * 10 + ch_num_table[c]
        
        if has_decimal:
            parsed_number_str = str(parsed_number) + '.'
            # plus one because it contain the point
            dec_start = has_decimal.start() + 1
            for c in test_str[dec_start:]:
                assert c in digits
                print(parsed_number_str)
                parsed_number_str += str(ch_num_table[c])
            parsed_number = float(parsed_number_str)

    except AssertionError:
        return test_str
    # print("Parsed", test_str)
    return parsed_number * sign
    
if __name__ == '__main__':
    assert parse_ch_num('七') == 7
    assert parse_ch_num('十二') == 12
    assert parse_ch_num('二百五') == 250
    assert parse_ch_num('兩千零二十四') == 2024
    assert parse_ch_num('二零二四') == 2024
    assert parse_ch_num('負十') == -10
    assert parse_ch_num('三點一四一五九') == 3.14159
    assert parse_ch_num('三十一萬四千一百五十九') == 31_4159
    assert parse_ch_num('正五億零五十五萬零五十五點零零五五') == 5_0055_0055.0055
    print('All pass')
