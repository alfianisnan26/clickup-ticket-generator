## Deskripsi
{description}

## Alur Penggunaan Tiket
### Pembuatan Tiket
#### Admin
- Menambahkan tiket melalui template untuk tiket ini
- Menambahkan nama tiket dengan format: [Level][PX-LY] Level Tracker
- Tags: level 
### Status: OPEN
#### Siswa:
- Memastikan assignee sesuai dengan akun siswa (diri sendiri)
- Menggeser status **OPEN ➝ TODO**
### Status: TODO
#### Siswa
- Menambahkan tanggal akan dimulainya proyek (pada **Dates > Start date**)
- Menambahkan deksripsi pada kolom komentar tentang proyek yang akan dibuat
- Menambahkan assigne untuk Checklist Approval Men96838524tor
- Menggeser status **TODO ➝ Mentoring**
### Status: MENTORING
#### Siswa
- Melakukan proses pembuatan proyek
- Menulis rangkuman hasil proyek dan link dari proyek (tulis di kolom komentar)
- Menambahkan tanggal selesainya proyek (pada **Dates > Due date**)
#### Mentor
- Melakukan verifikasi pada proyek yang dikerjakan
- Menambahkan masukkan jika diperlukan pada kolom komentar
- Menambahkan assignee untuk Checklist Approval **Reviewer**
- Checklist Approval **Mentoring** (jika sudah terverifikasi)
- Menggeser status **MENTORING ➝ APPROVING**
- Menggeser status **MENTORING ➝ TODO**: dengan komentar untuk menunjukkan pembelajaran ulang.
### Status: APPROVING
#### Approver
- Melakukan verifikasi pada data pada tiket meliputi checklist, status, record dari tiket dan histori.
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