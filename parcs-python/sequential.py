import time

def find_all_occurrences(text, pattern):
    indices = []
    start = 0
    while True:
        idx = text.find(pattern, start)
        if idx == -1:
            break
        indices.append(idx)
        start = idx + 1
    return indices

def main():
    pattern = "PARCS_TARGET_KEY"
    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read()

    t_start = time.perf_counter()
    matches = find_all_occurrences(text, pattern)
    elapsed = time.perf_counter() - t_start

    print(f"[Sequential] Знайдено входжень: {len(matches)}")
    print(f"[Sequential] Перші 5 позицій: {matches[:5]}")
    print(f"[Sequential] Час виконання: {elapsed:.4f} сек")

if __name__ == "__main__":
    main()