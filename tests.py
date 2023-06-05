import re


def is_japanese(look_up_word: str) -> str|Exception:
    # Unicode range for Hiragana, Katakana and Kanji (HKK)
    hkk = r'[\u3040-\u30FF\u4E00-\u9FFF]'
    if re.match(f'^{hkk}+$', look_up_word) is not None:
        return "OK"
    else:
         raise Exception("There was an issue with your input. Use Japanese characters only.")

def main():
    assert is_japanese('こんにちは') == True  # True
    assert is_japanese('バナナ') == True # True
    assert is_japanese('猫') == True # True
    assert is_japanese('cat') == False #False
    assert is_japanese('はハppyTime') == False # False
    
if __name__ == "__main__":
    main()
    print('No errors fouund. All test functions passed')