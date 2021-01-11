Kita perlu cek dulu apabila key berada dalam result:
```
for result in result_data['results']:
    if 'url' in result:
      print(result['url'])
```
Keluaran program:
```
https://www.realtor.com/realestateandhomes-detail/19207-120th-Ave_Jamaica_NY_11412_M35290-82139
```
Sebagai alternatif solusi lain, kalau kita asumsikan letak key seperti address tidak tahu di mana, maka kita telusuri setiap elemen dalam result_data['results'] dan cek apabila terdapat key address. Kita juga dapat menggunakan list comprehension:
```
[x['address'] for x in result_data['results'] if 'address' in x]
Ini mengambil semua 'address' untuk setiap elemen di result_data['results'] apabila ada.
```
Keluaran program:
```
[{'type': 'PostalAddress', 'streetAddress': '192-07 120th Ave', 'addressLocality': 'Jamaica', 'addressRegion': 'NY', 'postalCode': '11412'}]
```
Contoh apabila ingin mengambil semua value dari key url:
```
[x['url'] for x in result_data['results'] if 'url' in x]
```
Keluaran program:
```
['https://www.realtor.com/realestateandhomes-detail/19207-120th-Ave_Jamaica_NY_11412_M35290-82139']
```
Sedangkan apabila kita asumsikan addressnya hanya terdapat pada elemen urutan ke-3, maka kita dapat akses dengan:
```
result_data['results'][2]['address']
```
Keluaran program:
```
{'type': 'PostalAddress', 'streetAddress': '192-07 120th Ave', 'addressLocality': 'Jamaica', 'addressRegion': 'NY', 'postalCode': '11412'}
```
