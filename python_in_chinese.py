import sys
import re

word_table = [
#代數
    ('+', '加'),
    ('-', '減'),
    ('*', '乘'),
    ('/', '除'),
    ('%', '模'),
    ('**', '冪'),
    ('//', '底除'),
#位元
    ('~', '反相'),
    ('&', '位元與'),
    ('|', '位元或'),
    ('^', '位元異或'),
    ('<<', '左移'),
    ('>>', '右移'),
#賦值
    ('=', '設成'),
    ('+=', '加並設成'),
    ('-=', '減並設成'),
    ('*=', '乘並設成'),
    ('/=', '除並設成'),
    ('%=', '模並設成'),
    ('**=', '冪並設成'),
    ('//=', '底除並設成'),
#位元
#比較
    ('==', '等於'),
    ('!=', '不等於'),
    ('>', '大於'),
    ('<', '小於'),
    ('>=', '大於等於'),
    ('<=', '小於等於'),
#邏輯
    ('not', '非'),
    ('and', '且'),
    ('or', '或'),
#身分
    ('is', '是'),
    ('is not', '不是'),
#成員
    ('in', '在'),
    ('not in', '不在'),
#關鍵字
    ('False', '假'),
    ('True', '真'),
    ('None', '無'),
    ('if', '若'),
    ('else', '否'),
    ('elif', '又若'),
    ('from', '從'),
    ('import', '引入'),
    ('return', '回傳'),
    ('yield', '生成'),
    ('pass', '略'),
    ('await', '等待'),
    ('raise', '抛出'),
    ('assert', '斷言'),
    ('break', '脫出'),
    ('continue', '繼續'),
    ('try', '試'),
    ('except', '接'),
    ('finally', '最後'),
    ('while', '當'),
    ('for', '凡'),
    ('in', '在'),
    ('with', '以'),
    ('as', '作為'),
    ('class', '類別'),
    ('def', '函式'),
    ('lambda', 'lambda'),
    ('async', '異步'),
    ('nonlocal', '外域'),
    ('global', '全域'),
    ('del', '刪'),
#內建函數
    ('abs', '絕對值'),
    ('aiter', '異步迭代'),
    ('all', '全部'),
    ('anext', '異步下一項'),
    ('any', '任何'),
    ('ascii', 'ascii'),
    ('bin', '二進位'),
    ('bool', '布林值'),
    ('breakpoint', '中斷點'),
    ('bytearray', '位元組陣列'),
    ('bytes', '位元組串'),
    ('callable', '可呼叫'),
    ('chr', '轉字元'),
    ('classmethod', '類方法'),
    ('compile', '編譯'),
    ('complex', '複數'),
    ('delattr', '刪屬性'),
    ('dict', '字典'),
    ('dir', '名稱'),
    ('divmod', '除模'),
    ('enumerate', '列舉'),
    ('eval', '求值'),
    ('exec', '執行'),
    ('filter', '篩'),
    ('float', '浮點數'),
    ('format', '格式'),
    ('frozenset', '凍集合'),
    ('getattr', '取屬性'),
    ('globals', '全域表'),
    ('hasattr', '有屬性'),
    ('hash', '雜湊'),
    ('help', '幫助'),
    ('hex', '十六進位'),
    ('id', '標識值'),
    ('input', '輸入'),
    ('int', '整數'),
    ('isinstance', '是實例'),
    ('issubclass', '是子類'),
    ('iter', '迭代'),
    ('len', '長度'),
    ('list', '串列'),
    ('locals', '局域表'),
    ('map', '映射'),
    ('max', '最大值'),
    ('memoryview', '記體視圖'),
    ('min', '最小值'),
    ('next', '下一項'),
    ('object', '物件'),
    ('oct', '八進位'),
    ('open', '開啟'),
    ('ord', '轉編碼'),
    ('pow', '次方'),
    ('print', '印出'),
    ('property', '特征屬性'),
    ('range', '範圍'),
    ('repr', '表示'),
    ('reversed', '逆'),
    ('round', '捨入'),
    ('set', '集合'),
    ('setattr', '設屬性'),
    ('slice', '切片'),
    ('sorted', '排序'),
    ('staticmethod', '靜態方法'),
    ('str', '字串'),
    ('sum', '總和'),
    ('super', '從父類'),
    ('tuple', '元组'),
    ('type', '型別'),
    ('vars', '屬性字典'),
    ('zip', '鏈'),
# 分離符
    (':', '則'),
    (':', '定義為'),
    (':', '預期為'),
    ('.', '的')
]

# sort table with descending chinese string len
word_table = sorted(
    word_table,
    key=lambda p: len(p[1]),
    reverse=True
)

translation_dict = {
    ch_word: word
    for word, ch_word in word_table
}

comment_pattern = r'#.+'

# make splitter pattern
splitter_pattern = r'|'.join([
        # whitespaces
        r'(\s+)',
        # string literals
        r'([fru]?\".+\")',
        r'([fru]?\'.+\')',
        f'[\'\"]{3}.+[\'\"]{3}',
        # delimiters
        r'([\\\(\)\{\}\[\]\"\'\:\.,@])',
    ] + [
        # chinese translated delimiter and operators
        f'({cn_word})'
        for word, cn_word in word_table
        if not word.isalpha() and ' ' not in word
    ]
)
splitter_pattern = re.compile(splitter_pattern)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Need a path to the script')
    else:
        with open(sys.argv[1], 'r', encoding='utf8') as f:
            zh_script = f.read()
    
        zh_script = re.sub(comment_pattern, '', zh_script)

        zh_script_splits = [
            s
            for s in re.split(splitter_pattern, zh_script)
            if s != '' and s is not None
        ]
        # print(zh_script_splits)

        script_splits = [
            translation_dict.get(s, s)
            for s in zh_script_splits
        ]
        try:
            exec(''.join(script_splits))
        except Exception as e:
            print(''.join(script_splits))
            raise e
