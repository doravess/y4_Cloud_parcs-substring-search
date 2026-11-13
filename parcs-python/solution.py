import time
from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        pattern = "PARCS_TARGET_KEY"
        text = self.read_input()
        n = len(text)
        m = len(pattern)
        num_workers = len(self.workers)

        t_start = time.perf_counter()

        # Розбиваємо текст на частини із перекриттям (m - 1), щоб не втратити збіги на стиках
        chunk_size = n // num_workers
        mapped = []

        for i in range(num_workers):
            start_idx = i * chunk_size
            if i == num_workers - 1:
                end_idx = n
            else:
                end_idx = min(n, (i + 1) * chunk_size + (m - 1))

            sub_text = text[start_idx:end_idx]
            mapped.append(self.workers[i].mymap(sub_text, pattern, start_idx))

        # Збір та об'єднання результатів від усіх воркерів
        all_indices = set()
        for future in mapped:
            worker_indices = future.value
            all_indices.update(worker_indices)

        sorted_indices = sorted(all_indices)
        elapsed = time.perf_counter() - t_start

        self.write_output(sorted_indices, elapsed, num_workers)

    @staticmethod
    @expose
    def mymap(sub_text, pattern, offset):
        local_matches = []
        start = 0
        while True:
            idx = sub_text.find(pattern, start)
            if idx == -1:
                break
            local_matches.append(offset + idx)
            start = idx + 1
        return local_matches

    def read_input(self):
        with open(self.input_file_name, "r", encoding="utf-8") as f:
            return f.read()

    def write_output(self, indices, elapsed, num_workers):
        with open(self.output_file_name, "w", encoding="utf-8") as f:
            f.write(f"Workers: {num_workers}\n")
            f.write(f"Total matches: {len(indices)}\n")
            f.write(f"Execution time: {elapsed:.4f} sec\n")
            f.write(f"First 10 positions: {indices[:10]}\n")
        print(f"[PARCS | {num_workers} workers] Знайдено: {len(indices)} | Час: {elapsed:.4f} сек")