import os
import sys

VOCAB = {
    "the", "a", "an",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us",
    "my", "your", "his", "our", "their",
    "this", "that",
    "and", "or", "but", "so", "if",
    "not", "then", "now", "here", "there",
    "in", "on", "at", "to", "from", "with", "by", "of", "for",
    "what", "who", "where", "why", "how",
    "is", "are", "was", "were", "be", "have", "has", "had", "can", "will",
    "go", "come", "see", "get", "make", "say", "know", "think", "want", "need",
    "like", "love", "find", "give", "take", "work", "ask", "help", "put",
    "went", "came", "got", "made", "said", "knew",
    "man", "woman", "child", "day", "time", "world", "house", "water", "food",
    "life", "way", "thing",
    "good", "big", "old", "new", "long", "right", "small",
    "<EOL>",
}


def check_directory(directory):
    """Return dict mapping filename -> list of bad tokens for each .txt file."""
    violations = {}
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        bad = [
            token for token in text.split()
            if (token if token == "<EOL>" else token.lower()) not in VOCAB
        ]
        if bad:
            violations[filename] = bad
    return violations


def main(directory="datasets"):
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' directory not found")
        sys.exit(1)
    violations = check_directory(directory)
    if not violations:
        print("All files OK")
        sys.exit(0)
    for filename, bad_tokens in violations.items():
        unique = sorted(set(bad_tokens))
        print(f"FAIL {filename}: {len(bad_tokens)} violation(s) — {unique}")
    sys.exit(1)


if __name__ == "__main__":
    main()
