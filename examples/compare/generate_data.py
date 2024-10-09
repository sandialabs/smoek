import smoek as smk

# p-median

sizes = [100, 1000, 3000, 9000]

for size in sizes:
    d = {}
    for n in range(size):
        for m in range(size):
            d[n,m] = 1.0 + 1.0/(n+m+1.0)
    print("p-median",size)
    smk.store_data_to_json(filename=f'data/pmedian3_{size}.json', d=d)
    smk.store_data_to_json(filename=f'data/pmedian4_{size}.json', d=d)

