import os
import re
import eyed3

def has_chinese(text):
    """判断字符串是否包含中文"""
    return re.search(r'[\u4e00-\u9fff]', text) is not None

def is_messy_chinese(text):
    """判断是不是中文乱码"""
    if not text:
        return False
    if has_chinese(text):
        return False
    # 判断是否有大量不可打印字符（乱码的特征）
    messy_ratio = sum(1 for c in text if ord(c) > 127) / len(text)
    return messy_ratio > 0.3

def detect_and_decode(raw_text):
    """尝试用各种编码解码"""
    encodings = ['gbk', 'gb2312', 'big5', 'utf-8']
    for enc in encodings:
        try:
            decoded = raw_text.encode('latin1').decode(enc)
            if has_chinese(decoded):
                return decoded, enc
        except:
            continue
    return None, None

def fix_tags(mp3_file):
    audio = eyed3.load(mp3_file)
    if not audio or not audio.tag:
        print(f"[跳过] 无标签: {mp3_file}")
        return

    modified = False
    tag = audio.tag

    for attr_name in ['title', 'artist', 'album']:
        raw_value = getattr(tag, attr_name)
        if not raw_value:
            continue

        # 如果是乱码中文，尝试修复
        if is_messy_chinese(raw_value):
            fixed, enc = detect_and_decode(raw_value)
            if fixed:
                setattr(tag, attr_name, fixed)
                print(f"[修复] {mp3_file} → {attr_name}: {raw_value} → {fixed} (编码: {enc})")
                modified = True
        # 否则，不修改
        else:
            print(f"[跳过] {mp3_file} → {attr_name}: {raw_value} (无需修复)")

    if modified:
        # 使用 ID3v2.4 + UTF-8 编码保存标签
        tag.save(version=(2, 4, 0), encoding='utf-8')
    else:
        print(f"[跳过] 无需修改: {mp3_file}")

def main():
    for filename in os.listdir('.'):
        if filename.lower().endswith('.mp3'):
            fix_tags(filename)

if __name__ == '__main__':
    main()
