## Alur Penggunaan Tiket
### Pembuatan Tiket
#### Siswa (sebagai coach)
- Mengganti nama tiket menjadi format [COACHING] #Nomor Urut | contoh: [Coaching] #1
- Memastikan tag coaching
### Status: OPEN
#### Siswa (sebagai coach)
- Memastikan assignee sesuai dengan akun siswa (diri sendiri)
- Menggeser status **OPEN ➝ TODO**
### Status: TODO
#### Siswa (sebagai coach)
- Menambahkan relasi tiket pada Relationship dengan jenis **WAITING ON** pada tiket siswa yang diberikan materi pelajaran (jika banyak siswa, baiknya meminta siswa untuk melakukan penambahan Relationships pada tiket ini dengan jenis **BLOCKING**)
- Menggeser status **TODO ➝ Mentoring**
### Status: MENTORING
#### Siswa (sebagai coach)
- Menambahkan tanggal kapan melakukan proses coaching (pada kolom **Dates ➝ Due Date**)
- Menambahkan refleksi diri jika diperlukan pada kolom komentar
- Menambahkan assignee untuk Checklist Approval **Reviewer**
- Menggeser status **MENTORING ➝ APPROVING**
### Status: APPROVING
#### Reviewer
- Melakukan verifikasi pada data pada tiket meliputi Checklist Approval, status, record dari tiket dan histori.
- Checklist Approval **Reviewer**
- Menggeser status **APPROVING ➝ APPROVED**
- Menggeser status **APPROVING ➝ TODO**: dengan komentar jika terdapat informasi yang kurang
- Menggeser status **APPROVING ➝ BLOCKED**: dengan komentar jika dinyatakan tidak berhak mendapatkan nilai coaching.
### Status: APPROVED
#### Siswa (sebagai mentor)
- Menggeser status **APPROVED ➝ DONE**
- Note: Dilarang menggeser status **BLOCKED**.
### Status: DONE
