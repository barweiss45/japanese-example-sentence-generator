import re


def is_japanese(string):
    # Unicode range for Hiragana, Katakana and Kanji (HKK)
    hkk = r'[\u3040-\u30FF\u4E00-\u9FFF]'
    
    # Match the entire string with the above range
    return re.match(f'^{hkk}+$', string) is not None

def main():
    assert is_japanese('こんにちは') == True  # True
    assert is_japanese('バナナ') == True # True
    assert is_japanese('猫') == True # True
    assert is_japanese('cat') == False #False
    assert is_japanese('はハppyTime') == False # False
    
if __name__ == "__main__":
    main()
    print('No errors fouund. All test functions passed')