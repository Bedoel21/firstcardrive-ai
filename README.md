# 🚗 FirstCarDrive AI: Smart Recommendation Agent

FirstCarDrive AI adalah aplikasi asisten cerdas berbasis Generative AI yang dirancang khusus untuk membantu pembeli mobil pertama (*first-time buyer*) di Indonesia menemukan kendaraan ideal mereka. Aplikasi ini mengintegrasikan antarmuka interaktif Streamlit dengan Gemini API sebagai mesin penalaran utama (*Reasoning Engine*) dan Exa API untuk pencarian web berbasis *neural* secara *real-time*.

## 🌟 Fitur Utama
- **AI Agent & Function Calling**: Agen AI tidak hanya mengobrol pasif, tetapi mampu memanggil alat luar secara otonom ketika membutuhkan data valid.
- **Real-Time Neural Search**: Terintegrasi dengan **Exa API** untuk melakukan penelusuran harga pasar, spesifikasi, dan *review* mobil terkini langsung dari situs otomotif Indonesia.
- **Konteks Multimodal Terstruktur**: Sidebar Streamlit menangkap data krusial (*budget*, tipe bodi, keperluan) sebagai basis prompt yang kokoh bagi model.
- **Robust Session State**: Percakapan multiturn terjaga dengan aman memanfaatkan manajemen *state* Streamlit demi menghindari kehilangan data saat terjadi *rerun*.

## 🏗️ Arsitektur Sistem
Aplikasi ini menggunakan kerangka kerja modular dengan alur sebagai berikut:
1. Pengguna memasukkan kriteria pada *sidebar* dan mengetik detail cerita kebutuhan pada *chatbox*.
2. **Gemini API (`gemini-2.5-flash`)** menerima instruksi sistem yang ketat (*Prompt Engineering*) dan menganalisis kebutuhan pengguna.
3. Jika membutuhkan data eksternal, Gemini secara otomatis memicu fungsi **Function Calling** menuju **Exa API**.
4. Hasil pencarian web digabungkan ke dalam konteks penalaran untuk menghasilkan output rekomendasi terstruktur berformat Markdown estetik (Tabel, Blockquote, List).

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://firstcardrive-ai.streamlit.app/)

> 🌐 **Aplikasi Live URL:** [firstcardrive-ai.streamlit.app](https://firstcardrive-ai.streamlit.app/)

## 🚀 Cara Menjalankan Secara Lokal

### 1. Kloning Repositori
```bash
git clone [https://github.com/Bedoel21/firstcardrive-ai.git](https://github.com/Bedoel21/firstcardrive-ai.git)
cd firstcardrive-ai
