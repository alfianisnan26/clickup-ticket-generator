## Alur Penggunaan Tiket
### Pembuatan Tiket
#### Admin
- Menambahkan tiket melalui template untuk tiket ini
- Menambahkan nama tiket dengan format: [LEVEL | PX-LY] Level Tracker
- Tags: level
### Status: OPEN
#### Siswa
- Memastikan assignee sesuai dengan akun siswa (diri sendiri)
- Menggeser status **OPEN ➝ TODO**
### Status: TODO
#### Siswa
- Menambahkan tanggal kapan melakukan proses pembelajaran pertama kali (pada kolom **Dates ➝ Start Date**)
- Melakukan proses pembelajaran (dari subtask)
- Menulis rangkuman hasil pembelajaran (tulis di kolom komentar)
- Menambahkan assignee untuk Checklist Approval **Mentor**
- Menggeser status **TODO ➝ Mentoring**
### Status: MENTORING
#### Siswa
- Melakukan review materi dari seluruh subtask bersama mentor
- Menambahkan tanggal kapan melakukan proses permintaan approval mentoring (pada kolom **Dates ➝ Due Date**)
#### Mentor
- Melakukan verifikasi pada setiap subtask
- Menambahkan masukkan jika diperlukan pada kolom komentar
- Menambahkan assignee untuk Checklist Approval **Reviewer**
- Checklist Approval **Mentor** (jika sudah terverifikasi)
- Menggeser status **MENTORING ➝ APPROVING**
- Menggeser status **MENTORING ➝ TODO**: dengan komentar untuk menunjukkan pembelajaran ulang.
### Status: APPROVING
#### Approver
- Melakukan verifikasi pada data pada tiket meliputi Checklist Approval, status, record dari tiket dan histori.
- Checklist Approval **Reviewer**
- Menggeser status **APPROVING ➝ APPROVED**
- Menggeser status **APPROVING ➝ MENTORING** atau **APPROVING ➝ TODO**: dengan komentar, jika terdapat informasi yang kurang, atau dinyatakan perlu mengulang untuk materi ini.
- Menggeser status **APPROVING ➝ BLOCKED**: dengan komentar, jika dinyatakan tidak boleh diluluskan untuk level ini.
### Status: APPROVED
#### Siswa
- Mengecek masukkan (jika ada)
- Menggeser status **APPROVED ➝ DONE**
- Note: Mohon untuk tidak menggeser lagi status jika approver menggeser status pada **BLOCKED**.
### Status: DONE