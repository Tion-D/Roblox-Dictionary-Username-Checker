import requests
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import sys

file_lock = Lock()
stats_lock = Lock()

stats = {
    'available': 0,
    'taken': 0,
    'errors': 0,
    'checked': 0
}

def download_wordlist():
    """Download a comprehensive English word list"""
    print("Downloading English word list...")
    
    sources = [
        "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt",
        "https://www.mit.edu/~ecprice/wordlist.10000"
    ]
    
    for url in sources:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                words = response.text.strip().split('\n')
                words = [w.strip().lower() for w in words if w.strip()]
                print(f"✓ Downloaded {len(words)} words")
                return words
        except Exception as e:
            print(f"Failed to download from {url.split('/')[-1]}: {e}")
            continue
    
    return None

def load_or_download_words():
    wordlist_file = Path("english_words.txt")
    
    if wordlist_file.exists():
        print("Loading word list from file...")
        with open(wordlist_file, 'r') as f:
            words = [line.strip().lower() for line in f if line.strip()]
        print(f"✓ Loaded {len(words)} words")
        return words
    else:
        words = download_wordlist()
        if words:
            with open(wordlist_file, 'w') as f:
                f.write('\n'.join(words))
            print(f"✓ Saved word list to {wordlist_file}")
        return words

def filter_words(words, min_length=3, max_length=20):
    filtered = []
    
    for word in words:
        if len(word) < min_length or len(word) > max_length:
            continue
        
        if not word.isalpha() or not word[0].isalpha():
            continue
        
        filtered.append(word)
    
    return filtered

def check_username_available(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.roblox.com",
        "Referer": "https://www.roblox.com/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                return True
            elif data.get("code") in [1, 2, 10]:
                return False
            else:
                return None
        elif response.status_code == 429:
            time.sleep(2)
            return None
        else:
            return None
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        return None

def check_username_thread(username):
    result = check_username_available(username)
    
    with stats_lock:
        stats['checked'] += 1
        if result is True:
            stats['available'] += 1
        elif result is False:
            stats['taken'] += 1
        else:
            stats['errors'] += 1
    
    return username, result

def save_available_username(username):
    with file_lock:
        with open("available_usernames.txt", "a") as f:
            f.write(f"{username}\n")

def check_words_multithreaded(words, max_threads=20):
    print(f"\n{'='*60}")
    print(f"Checking {len(words)} dictionary words with {max_threads} threads...")
    print(f"{'='*60}\n")
    
    available_usernames = []
    start_time = time.time()
    
    Path("available_usernames.txt").unlink(missing_ok=True)
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_word = {executor.submit(check_username_thread, word): word for word in words}
        
        for future in as_completed(future_to_word):
            word = future_to_word[future]
            try:
                username, result = future.result()
                
                if result is True:
                    print(f"✓ AVAILABLE: {username}")
                    available_usernames.append(username)
                    save_available_username(username)
                elif result is False:
                    print(f"✗ Taken: {username}")
                else:
                    print(f"? Error: {username}")
                
                if stats['checked'] % 25 == 0:
                    elapsed = time.time() - start_time
                    rate = stats['checked'] / elapsed if elapsed > 0 else 0
                    print(f"\n📊 Progress: {stats['checked']}/{len(words)} | "
                          f"Available: {stats['available']} | "
                          f"Rate: {rate:.1f} checks/sec\n")
                
            except Exception as e:
                print(f"Exception checking {word}: {e}")
    
    elapsed_time = time.time() - start_time
    
    return available_usernames, elapsed_time

def main():
    print("=" * 60)
    print("Roblox Fast Dictionary Username Finder")
    print("=" * 60)
    print("\n🚀 Multithreaded for maximum speed!\n")
    
    # Load words
    words = load_or_download_words()
    
    if not words:
        print("\n❌ Could not load word list.")
        return
    
    print(f"\n📚 Total words in dictionary: {len(words)}")
    
    print("\n" + "="*60)
    print("Filter Options:")
    print("="*60)
    
    try:
        min_len = int(input("Minimum word length (default 4): ").strip() or "4")
        max_len = int(input("Maximum word length (default 10): ").strip() or "10")
        max_checks = int(input("Maximum words to check (default 100000): ").strip() or "100000")
        threads = int(input("Number of threads (default 20, max 50): ").strip() or "20")
        threads = min(threads, 50)
    except ValueError:
        min_len, max_len, max_checks, threads = 4, 10, 500, 20
    
    print(f"\nFiltering words (length {min_len}-{max_len})...")
    filtered_words = filter_words(words, min_len, max_len)
    print(f"✓ {len(filtered_words)} words match criteria")
    
    if len(filtered_words) == 0:
        print("No words match your criteria!")
        return
    
    print("\nHow should we check the words?")
    print("1. Shortest first (more likely to be taken)")
    print("2. Longest first")
    print("3. Random order (recommended)")
    print("4. Alphabetical")
    
    choice = input("\nChoice (default 3): ").strip() or "3"
    
    if choice == "1":
        filtered_words.sort(key=len)
    elif choice == "2":
        filtered_words.sort(key=len, reverse=True)
    elif choice == "3":
        import random
        random.shuffle(filtered_words)
    elif choice == "4":
        filtered_words.sort()
    
    words_to_check = filtered_words[:max_checks]
    
    print(f"\nFirst 20 words to check: {', '.join(words_to_check[:20])}")
    input("\nPress Enter to start checking...")
    
    available, elapsed = check_words_multithreaded(words_to_check, threads)
    
    print(f"\n{'='*60}")
    print("RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"⏱  Time elapsed:  {elapsed:.1f} seconds")
    print(f"⚡ Check rate:    {stats['checked']/elapsed:.1f} usernames/second")
    print(f"✓  Available:     {stats['available']}")
    print(f"✗  Taken:         {stats['taken']}")
    print(f"?  Errors:        {stats['errors']}")
    
    if available:
        print(f"\n🎉 Found {len(available)} available usernames:")
        for word in sorted(available, key=len):
            print(f"  • {word}")
        print(f"\n✓ Saved to: available_usernames.txt")
    else:
        print("\n😞 No available usernames found.")
        if stats['errors'] > stats['taken']:
            print("⚠  Many errors occurred - there may be network/API issues.")
        else:
            print("💡 Try checking more words or adjusting the length range!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        print(f"Checked {stats['checked']} usernames before stopping")
        if stats['available'] > 0:
            print(f"Found {stats['available']} available - saved to available_usernames.txt")