@echo off
rem Ghep giong doc + nhac nen (tu dong ha nho nhac khi co giong) thanh am thanh hoan chinh.
rem Dung:  ghep_am_thanh.bat            -> tao am_thanh_hoan_chinh.m4a
rem        ghep_am_thanh.bat video.mp4  -> ghep luon vao video (video khong co tieng) thanh FRAS-AI_gioi_thieu_hoan_chinh.mp4
set VOICE=neu_ngay_luc_nay_nha_ban_boc_chay_va_tran_ngap_d95a9b02-5c9b-4840-9447-1565e60d2ce5.mp3
ffmpeg -y -i "%VOICE%" -i nhac_nen.wav -filter_complex "[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo,volume=1.0,asplit=2[v1][v2];[1:a]volume=0.55[m];[m][v1]sidechaincompress=threshold=0.02:ratio=8:attack=40:release=700:makeup=1[md];[v2][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=9[a]" -map "[a]" -c:a aac -b:a 256k am_thanh_hoan_chinh.m4a
if "%~1"=="" goto :eof
ffmpeg -y -i "%~1" -i am_thanh_hoan_chinh.m4a -map 0:v -map 1:a -c:v copy -c:a copy -shortest -movflags +faststart FRAS-AI_gioi_thieu_hoan_chinh.mp4
