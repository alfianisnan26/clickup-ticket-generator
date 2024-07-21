## Alur Penggunaan Tiket
### Pembuatan Tiket
#### Siswa (sebagai mentor)
- Mengganti nama tiket menjadi format [MENTORING] Nama Mentee | contoh: [MENTORING] Alfian Badrul Isnan
- Memastikan memiliki tag mentoring
### Status: OPEN
#### Siswa (sebagai mentor)
- Memastikan assignee sesuai dengan akun siswa (diri sendiri)
- Menggeser status **OPEN ➝ TODO**
### Status: TODO
#### Siswa (sebagai mentor)
- Menambahkan relasi tiket pada Relationship dengan jenis **WAITING ON** pada tiket siswa yang diberikan materi pelajaran
- Menggeser status **TODO ➝ Mentoring**
### Status: MENTORING
#### Siswa (sebagai mentor)
- Menambahkan tanggal kapan melakukan proses mentoring (pada kolom **Dates ➝ Due Date**)
- Menambahkan refleksi diri jika diperlukan pada kolom komentar
- Menambahkan assignee untuk Checklist Approval **Reviewer**
- Menggeser status **MENTORING ➝ APPROVING**
### Status: APPROVING
#### Approver
- Melakukan verifikasi pada data pada tiket meliputi checklist, status, record dari tiket dan histori.
- Checklist Approval **Reviewer**
- Menggeser status **APPROVING ➝ APPROVED**
- Menggeser status **APPROVING ➝ TODO**: dengan komentar jika terdapat informasi yang kurang
- Menggeser status **APPROVING ➝ BLOCKED**: dengan komentar jika dinyatakan tidak berhak mendapatkan nilai mentoring.
### Status: APPROVED
- Siswa (sebagai mentor)
- Menggeser status **APPROVED ➝ DONE**
- Note: Dilarang menggeser status BLOCKED. 
### Status: DONE