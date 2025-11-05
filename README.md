# 🚀 Roblox Fast Username Checker

**The fastest way to find available Roblox usernames from dictionary words!**

## Quick Start

```bash
pip install requests
python main.py
```

## Features

- ⚡ **Multithreaded** - Check 20+ usernames simultaneously
- 🎯 **Smart endpoint** - Uses Roblox's validation API with proper parameters
- 📚 **370,000+ words** - Automatically downloads comprehensive dictionary
- 💾 **Auto-save** - Available usernames saved immediately
- 📊 **Live stats** - Real-time progress and success rate

## How Fast Is It?

With 20 threads (default):
- **~15-30 usernames/second**
- 500 usernames checked in **~20-40 seconds**
- 1000 usernames checked in **~40-90 seconds**

Compare to single-threaded: ~1 username/second 😴

## Example Session

```
Minimum word length: 5
Maximum word length: 8
Maximum words to check: 1000
Number of threads: 20

✓ AVAILABLE: zephyr
✗ Taken: shadow
✓ AVAILABLE: quasar
? Error: test
✗ Taken: legend

📊 Progress: 500/1000 | Available: 12 | Rate: 22.3 checks/sec
```

## Tips for Best Results

1. **Start with 500-1000 checks** to see what's available
2. **Use 6-10 character words** - sweet spot between unique and not-too-long
3. **Random order** works best for variety
4. **20-30 threads** is optimal (more may cause rate limiting)
5. **Shorter words** are almost always taken
6. **Look for uncommon words** - "azure", "nexus", "cipher" over "cool", "king", "fire"

## What the codes mean:

- `✓ AVAILABLE` - Username is free! Claim it quick!
- `✗ Taken` - Already registered
- `? Error` - Network issue or rate limit (temporary)

## Troubleshooting

**Getting lots of errors?**
- Reduce thread count (try 10 threads)
- Check your internet connection
- Wait a few minutes if rate limited

**No available usernames?**
- Try longer words (8-12 characters)
- Check more words (2000+)
- Use random order
- Try less common words

## Word Length Strategy

| Length | Availability | Examples |
|--------|-------------|----------|
| 3-4 | Almost none | All taken |
| 5-6 | Very rare | "azure", "prism" |
| 7-8 | **Best odds** | "nebula", "phantom" |
| 9-10 | Good chance | "labyrinth", "serendipity" |
| 11+ | Very likely | Most available |

## Files Created

- `available_usernames.txt` - Your found usernames (auto-saved)
- `english_words.txt` - Downloaded dictionary (reused)

---

Good luck finding your perfect username! 🎮✨
