#!/usr/bin/env python3
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import pathlib
import yt_dlp

def video_indir_arkaplanda(urls_text, secim, text_widget, btn):
    urls = urls_text.strip().split()
    if not urls:
        messagebox.showwarning("Uyarı", "Lütfen en az bir video bağlantısı girin!")
        btn.config(state="normal")
        return

    text_widget.config(state="normal")
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, f"📦 Toplam {len(urls)} medya işleniyor ({secim})...\n\n")
    text_widget.config(state="disabled")

    # İndirilenler klasörünü otomatik tespit et
    indir_klasoru = str(pathlib.Path.home() / "Downloads")
    if not os.path.exists(indir_klasoru):
        indir_klasoru = str(pathlib.Path.home() / "İndirilenler")

    def progress_hook(d):
        if d['status'] == 'downloading':
            yuzde = d.get('_percent_str', '0%').strip()
            hiz = d.get('_speed_str', 'Bilinmiyor').strip()
            tahmini_sure = d.get('_eta_str', 'Bilinmiyor').strip()
            
            text_widget.config(state="normal")
            text_widget.insert(tk.END, f"⏳ İndiriliyor: %{yuzde} (Hız: {hiz}, Kalan: {tahmini_sure})\n")
            text_widget.config(state="disabled")
            text_widget.see(tk.END)
        elif d['status'] == 'finished':
            text_widget.config(state="normal")
            text_widget.insert(tk.END, f"✓ Dosya indirildi, birleştiriliyor/işleniyor...\n")
            text_widget.config(state="disabled")
            text_widget.see(tk.END)

    # Seçilen formata göre yt_dlp ayarları
    if secim == "Sadece Ses (MP3)":
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(indir_klasoru, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }
    elif secim == "Sadece Video (Sessiz)":
        ydl_opts = {
            'format': 'bestvideo',
            'outtmpl': os.path.join(indir_klasoru, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }
    elif secim == "Fotoğraf / Kapak":
        ydl_opts = {
            'writethumbnail': True,
            'skip_download': True,
            'outtmpl': os.path.join(indir_klasoru, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }
    else:  # Hem Ses Hem Video
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best/best',
            'outtmpl': os.path.join(indir_klasoru, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }

    for i, url in enumerate(urls, 1):
        text_widget.config(state="normal")
        text_widget.insert(tk.END, f"[{i}/{len(urls)}] Başlatılıyor: {url}\n")
        text_widget.config(state="disabled")
        text_widget.see(tk.END)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            text_widget.config(state="normal")
            text_widget.insert(tk.END, f"🎉 Başarıyla tamamlandı!\n\n")
            text_widget.config(state="disabled")
            text_widget.see(tk.END)

        except Exception as e:
            text_widget.config(state="normal")
            text_widget.insert(tk.END, f"❌ Hata oluştu: {e}\n\n")
            text_widget.config(state="disabled")

    # İşlem bittiğinde butonu tekrar aktif et (Uygulama kapanmaz, açık kalır)
    btn.config(state="normal")
    messagebox.showinfo("İşlem Tamam", "Tüm indirme işlemleri bitti! Dosyalar İndirilenler klasöründe.")

def baslat():
    btn.config(state="disabled")
    urls_text = text_input.get("1.0", tk.END)
    secim = format_secim.get()
    threading.Thread(target=video_indir_arkaplanda, args=(urls_text, secim, log_box, btn), daemon=True).start()

# --- ARAYÜZ TASARIMI ---
root = tk.Tk()
root.title("Evrensel Medya İndirici")
root.geometry("540x560")
root.configure(bg="#0f172a")

lbl_title = tk.Label(root, text="🎬 Evrensel Medya İndirici", font=("Arial", 16, "bold"), bg="#0f172a", fg="#f8fafc")
lbl_title.pack(pady=10)

# Format Seçim Menüsü
lbl_format = tk.Label(root, text="İndirme Türünü Seçin:", font=("Arial", 10, "bold"), bg="#0f172a", fg="#38bdf8")
lbl_format.pack()

format_secim = tk.StringVar(root)
format_secim.set("Hem Ses Hem Video")  # Varsayılan seçenek
secenekler = [
    "Hem Ses Hem Video", 
    "Sadece Ses (MP3)", 
    "Sadece Video (Sessiz)", 
    "Fotoğraf / Kapak"
]
dropdown = tk.OptionMenu(root, format_secim, *secenekler)
dropdown.config(bg="#1e293b", fg="white", font=("Arial", 10), relief=tk.FLAT, highlightthickness=0)
dropdown["menu"].config(bg="#1e293b", fg="white")
dropdown.pack(pady=5)

lbl_info = tk.Label(root, text="İstediğin kadar linki alt alta yapıştırabilirsin:", font=("Arial", 10), bg="#0f172a", fg="#94a3b8")
lbl_info.pack()

text_input = scrolledtext.ScrolledText(root, width=58, height=5, font=("Arial", 10), bg="#1e293b", fg="#fff", insertbackground="white")
text_input.pack(pady=5)

btn = tk.Button(root, text="📥 İndirmeyi Başlat", font=("Arial", 11, "bold"), bg="#10b981", fg="white", padx=15, pady=8, command=baslat, relief=tk.FLAT, cursor="hand2")
btn.pack(pady=5)

log_box = scrolledtext.ScrolledText(root, width=58, height=8, font=("Consolas", 9), bg="#020617", fg="#38bdf8", insertbackground="white")
log_box.pack(pady=10)
log_box.config(state="disabled")

root.mainloop()
