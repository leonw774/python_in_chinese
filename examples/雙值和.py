函式 解雙值和(數字串 預期為串列, 目標數 預期為整數) 定義為
    甲 設成 0
    乙 設成 長度(數字串)減1
    當 甲小於乙 則
        若 數字串[甲]加數字串[乙] 等於 目標數 則
            回傳 (甲, 乙)
        若 數字串[甲]加數字串[乙] 小於 目標數 則
            甲 加並設成 1
        否 則
            乙 減並設成 1
    回傳 無

# 測資
數字串 設成 [0, 2, 11, 19, 90]
印出(解雙值和(數字串, 21))
印出(解雙值和(數字串, 25))
