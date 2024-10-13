import os.path
import smoek as smk

# p-median

sizes = [10, 100, 1000, 3000, 9000]

for size in sizes:
    print("p-median",size)
    if not os.path.exists(f'data/pmedian3_{size}.json'):
        d = {}
        for n in range(size):
            for m in range(size):
                d[n,m] = 1.0 + 1.0/(n+m+1.0)
        smk.store_data_to_json(filename=f'data/pmedian3_{size}.json', d=d)

