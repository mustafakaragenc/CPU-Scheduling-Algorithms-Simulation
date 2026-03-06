,,,,,,,,,,,,,
import time
import random
import matplotlib.pyplot as plt
import sys
import tracemalloc  # Bellek ölçümü 

# Recursion limitini artırıyoruz (Worst Case senaryoları için )
sys.setrecursionlimit(10000)


#  ALGORİTMA TASARIMLARI


def bubble_sort(arr):
    n = len(arr)
    # Optimize edilmiş Bubble Sort (Best Case O(n) için)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[i] < arr[l]:
            largest = l
        if r < n and arr[largest] < arr[r]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

# Quick Sort (Random Pivot )
def quick_sort(arr, low, high):
    if low < high:
        rand_idx = random.randint(low, high)
        arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        pi = i + 1
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def run_quick_sort(arr):
    quick_sort(arr, 0, len(arr) - 1)


#  TEST SENARYOLARI VE ANALİZ


def run_tests_and_analyze():
    # Veri boyutları
    sizes = [100, 500, 1000, 1500, 2000] 
    
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": lambda x: merge_sort(x),
        "Heap Sort": heap_sort,
        "Quick Sort (Random)": run_quick_sort
    }

    # 3 Temel Durum (Senaryo)
    scenarios = {
        "Best Case (Sıralı)": "sorted",
        "Average Case (Rastgele)": "random",
        "Worst Case (Ters)": "reverse"
    }
    
    # Sonuçları saklayacağımız yapılar
    all_results = {}  # Zaman karmaşıklığı için
    memory_results = {} # Bellek karmaşıklığı için

    # Grafik oluşturma (1 Satır, 3 Sütun)
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Sıralama Algoritmaları: Durum Analizleri (Time Complexity)', fontsize=16)

    print("TESTLER BAŞLIYOR... (Time & Space Complexity Hesaplanıyor)\n" + "="*50)

    for idx, (scenario_name, scenario_type) in enumerate(scenarios.items()):
        print(f"\n>>> SENARYO: {scenario_name} çalıştırılıyor...")
        
        scenario_time_results = {name: [] for name in algorithms}
        scenario_memory_results = {name: 0 for name in algorithms} # En büyük boyut için saklayacağız
        
        # Her algoritma için ölçüm yap
        for size in sizes:
            # Veri setini senaryoya göre oluştur
            base_data = [random.randint(0, 10000) for _ in range(size)]
            
            if scenario_type == "sorted":
                base_data.sort()
            elif scenario_type == "reverse":
                base_data.sort(reverse=True)
            
            for name, func in algorithms.items():
                test_data = base_data.copy() 
                
                # --- Bellek ve Zaman Ölçümü ---
                tracemalloc.start() # Bellek takibini başlat
                
                start_time = time.time()
                func(test_data)
                end_time = time.time()
                
                # Bellek kullanımını al (current, peak)
                _, peak_memory = tracemalloc.get_traced_memory()
                tracemalloc.stop() # Bellek takibini durdur
                # ------------------------------

                elapsed = end_time - start_time
                scenario_time_results[name].append(elapsed)
                
                # Sadece en büyük veri boyutunun bellek kullanımını raporda göstermek için kaydet
                if size == sizes[-1]:
                    scenario_memory_results[name] = peak_memory

        all_results[scenario_name] = scenario_time_results
        memory_results[scenario_name] = scenario_memory_results

        # Grafiği çiz
        ax = axes[idx]
        for name, times in scenario_time_results.items():
            ax.plot(sizes, times, marker='o', label=name)
        
        ax.set_title(scenario_name)
        ax.set_xlabel('Veri Boyutu')
        ax.set_ylabel('Süre (Saniye)')
        ax.grid(True)
        if idx == 0:
            ax.legend()

    plt.tight_layout()
    return all_results, memory_results, algorithms.keys()


# OTOMATİK METİNSEL ANALİZ RAPORU


def print_analysis_report(time_results, memory_results, algo_names):
    print("\n" + "="*60)
    print(f"{'SONUÇ ANALİZ RAPORU (TIME & SPACE)':^60}")
    print("="*60)

    for scenario, times_data in time_results.items():
        # En büyük veri boyutundaki süreleri al
        final_times = {name: times[-1] for name, times in times_data.items()}
        # İlgili senaryonun bellek verilerini al
        mem_data = memory_results[scenario]
        
        # En hızlı ve en yavaşı bul
        winner = min(final_times, key=final_times.get)
        loser = max(final_times, key=final_times.get)
        
        print(f"\n[{scenario}] DURUMU:")
        print("-" * 30)
        print(f" -> EN HIZLI (Time): {winner} ({final_times[winner]:.5f} sn)")
        print(f" -> EN YAVAŞ (Time): {loser} ({final_times[loser]:.5f} sn)")
        
        print("\n    BELLEK KULLANIMI (Peak Memory - Max Data Size):")
        for name in algo_names:
            mem_kb = mem_data[name] / 1024 # Byte'ı KB'a çevir
            print(f"    - {name:<20}: {mem_kb:.2f} KB")
        
        # Yorum Ekleme Mantığı
        if "Best" in scenario:
            if winner in ["Insertion Sort", "Bubble Sort"]:
                print("\n    YORUM: Liste zaten sıralı olduğunda O(n) çalışan basit algoritmalar çok hızlıdır.")
        elif "Worst" in scenario:
            if winner in ["Merge Sort", "Heap Sort", "Quick Sort (Random)"]:
                print(f"\n    YORUM: Ters sıralı veride O(n log n) olan algoritmalar ({winner} gibi) öne çıkar.")
        elif "Average" in scenario:
             print(f"\n    YORUM: Rastgele verilerde Random Quick Sort veya Merge Sort genellikle en iyi performansı gösterir.")

    print("\n" + "="*60)
    print("Grafik penceresi açıldı...")
    plt.show()

# Ana Program
if __name__ == "__main__":
    test_results, mem_results, algos = run_tests_and_analyze()
    print_analysis_report(test_results, mem_results, algos)