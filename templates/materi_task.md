## Deskripsi
{description}

## Alur Penggunaan Tiket
### Pembuatan Tiket
#### Admin
- Menambahkan tiket melalui template untuk tiket ini
- Menambahkan nama tiket dengan format: [MATERI | PX-LY.Z | KAT-MAT] Nama Pelajaran
- Menambahkan deskripsi
- Tags: materi + tag dari materi dan submateri yang sesuai
- Time Estimate: sesuai dengan tabel dibawah ini:
  - Effort 0.25 - 3h
  - Effort 0.75 - 4h30m
  - Effort 1 - 6h
  - Effort 2 - 12h
  - Effort n - 6*n
### Status: OPEN
#### Siswa
- Memastikan assignee sesuai dengan akun siswa (diri sendiri)
- Menggeser status **OPEN ➝ TODO**
### Status: TODO
#### Siswa
- Menambahkan assigne untuk Checklist Approval **Mentor**
- Menggeser status **TODO ➝ Mentoring**
- Menambahkan tanggal kapan akan m
### Status: MENTORING
#### Siswa
- Melakukan proses pembelajaran
- Menambahkan tanggal kapan melakukan proses pembelajaran (pada kolom **Dates ➝ Due Date**)
- Menulis rangkuman hasil pembelajaran (tulis di kolom komentar)
- Untuk jenis belajar mandiri, mohon pastikan telah memberikan rangkuman dan atau refleksi sebagai bukti dari belajar mandiri, bagian ini perlu di cek ulang oleh mentor dan approver
- Untuk jenis belajar mentoring, silahkan tambahkan Relationships dari tiket Mentoring dengan jenis **BLOCKING**
- Untuk jenis belajar coaching, silahkan tambahkan Relationships dari tiket Coaching dengan jenis **BLOCKING**
#### Mentor
- Melakukan verifikasi siswa telah menulis rangkuman (pada kolom komentar, terutama untuk belajar mandiri)
- Melakukan verifikasi pada tiket Relationships, jika tidak ada tiket yang dihubungkan dengan tipe Blocking untuk Mentoring, atau Coaching, dapat ditambahkan sesuai dengan syarat yang berlaku.
- Menambahkan masukkan jika diperlukan pada kolom komentar
- Menambahkan assignee untuk Checklist Approval **Reviewer**
- Checklist Approval **Mentor** (jika sudah terverifikasi)
- Menggeser status **MENTORING ➝ APPROVING**
- Menggeser status **MENTORING ➝ TODO**: dengan komentar untuk menunjukkan pembelajaran ulang.
### Status: APPROVING
#### Approver
- Melakukan verifikasi pada data pada tiket meliputi checklist approval, status, record dari tiket dan histori.
- Checklist Approval Reviewer
- Menggeser status **APPROVING ➝ APPROVED**
- Menggeser status **APPROVING ➝ MENTORING** atau APPROVING ➝ TODO: dengan komentar, jika terdapat informasi yang kurang, atau dinyatakan perlu mengulang untuk materi ini.
- Menggeser status **APPROVING ➝ BLOCKED**: dengan komentar, jika dinyatakan tidak boleh diluluskan untuk materi ini.
### Status: APPROVED
#### Siswa
- Mengecek masukkan (jika ada)
- Menggeser status **APPROVED** ➝ DONE
- Note: Mohon untuk tidak menggeser lagi status jika approver menggeser status pada BLOCKED.
### Status: DONE
#### Siswa
- Dapat menambahkan subtask Mentoring jika akan memberikan mentoring untuk mentee pada materi ini. Mohon tambahkan tiket menggunakan template Mentoring, baca info lebih lanjut pada tiket Mentoring
- Dapat menambahkan subtask Coaching jika akan memberikan coaching untuk partisipan pada materi ini. Mohon tambahkan tiket menggunakan template Coaching, baca info lebih lanjut pada tiket Coaching.