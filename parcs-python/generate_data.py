import random
import string

def generate_file(filename="input.txt", size_mb=50, pattern="PARCS_TARGET_KEY"):
    chunk_size = 1024 * 1024  # 1 МБ
    alphabet = string.ascii_letters + string.digits + " \n"
    total_bytes = size_mb * chunk_size
    written = 0
    inserted_count = 0

    with open(filename, "w", encoding="utf-8") as f:
        while written < total_bytes:
            # Генеруємо випадковий блок тексту
            block = "".join(random.choices(alphabet, k=min(chunk_size, total_bytes - written)))
            # Вставляємо шуканий підрядок у фіксовані та випадкові місця блоку
            if len(block) > 500:
                pos1 = 123
                pos2 = len(block) // 2
                block = block[:pos1] + pattern + block[pos1 + len(pattern):]
                block = block[:pos2] + pattern + block[pos2 + len(pattern):]
                inserted_count += 2
            f.write(block)
            written += len(block)

    print(f"Файл '{filename}' створено ({size_mb} МБ). Гарантовано вставлено входжень: {inserted_count}")

if __name__ == "__main__":
    generate_file()