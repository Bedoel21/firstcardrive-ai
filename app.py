import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from exa_py import Exa

# ==============================================================================
# 1. KONFIGURASI HALAMAN STREAMLIT (Wajib Paling Atas)
# ==============================================================================
st.set_page_config(page_title="FirstCarDrive AI", page_icon="🚗", layout="wide")

# ==============================================================================
# 2. INISIALISASI CLIENT MENGGUNAKAN SESSION STATE (Solusi Kebal Rerun)
# ==============================================================================
if "gemini_client" not in st.session_state or "exa_client" not in st.session_state:
    # Memuat file .env hanya SEKALI saat aplikasi pertama kali dinyalakan
    load_dotenv(override=True)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    EXA_API_KEY = os.getenv("EXA_API_KEY")

    if not GEMINI_API_KEY or not EXA_API_KEY:
        st.error("⚠️ **Konfigurasi API Key Gagal!**")
        st.markdown("""
        Aplikasi tidak dapat menemukan API Key di file `.env`. Periksa kembali nama file dan lokasinya.
        """)
        st.stop()
    
    # Simpan client secara permanen di dalam session_state agar tidak hilang saat rerun
    st.session_state.gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    st.session_state.exa_client = Exa(api_key=EXA_API_KEY)

# Menyediakan alias lokal agar kode di bawahnya tidak perlu banyak diubah
gemini_client = st.session_state.gemini_client
exa_client = st.session_state.exa_client

# ==============================================================================
# 3. FUNGSI TOOLS & ENGINE AGENT
# ==============================================================================
def cari_mobil_indonesia(query: str) -> str:
    """Mencari informasi mobil di Indonesia menggunakan Exa Neural Search."""
    try:
        full_query = f"{query} di Indonesia harga rupiah"
        response = exa_client.search(
            full_query,
            num_results=3,
            type="neural"
        )
        hasil = []
        for i, res in enumerate(response.results):
            cuplikan = res.text if hasattr(res, 'text') and res.text else "Tidak ada ringkasan teks."
            hasil.append(f"[{i+1}] Judul: {res.title}\nURL: {res.url}\nRingkasan: {cuplikan[:400]}...\n")
        return "\n".join(hasil) if hasil else "Tidak ditemukan hasil pencarian yang relevan."
    except Exception as e:
        return f"Error saat melakukan pencarian Exa: {str(e)}"

def jalankan_firstcar_agent(budget_max: int, tipe_mobil: str, keperluan: str, pesan_user: str) -> str:
    system_instruction = """
    Kamu adalah 'FirstCarDrive AI', seorang pakar otomotif senior dan asisten cerdas khusus pasar Indonesia. 
    Tugas utamamu adalah membantu pengguna awam (first-time buyer) menentukan mobil pertama yang paling cocok untuk mereka.
    
    ATURAN AGENT:
    1. Kamu memiliki akses ke tool 'cari_mobil_indonesia'. Gunakan tool ini WAJIB setiap kali pengguna meminta rekomendasi mobil baru/bekas, mengecek harga terkini di Indonesia, atau menanyakan review spesifik sebuah mobil. Jangan berasumsi tentang harga pasar terkini.
    2. Format jawabanmu HARUS sangat ramah, objektif, logis, dan kaya akan format Markdown yang estetik agar enak dibaca.
    
    STRUKTUR FORMAT JAWABAN (WAJIB DIIKUTI):
    - **Judul Utama**: Gunakan banner emoji yang menarik.
    - **Analisis Kebutuhan**: Bungkus ringkasan kondisi pengguna di dalam blockquote (`> `).
    - **Tabel Ringkasan**: Buatlah sebuah tabel Markdown singkat yang membandingkan Nama Mobil, Estimasi Harga, dan Rating Kecocokan.
    - **Detail Pilihan Mobil**: Gunakan format pemisah yang jelas (`---`). Kelompokkan kelebihan dan kekurangan secara kontras menggunakan bullet points.
    - **Rekomendasi Akhir & Tips**: Berikan kesimpulan dan tips praktis menggunakan numbered list.
    3. Jika pertanyaan pengguna di luar dunia otomotif atau pemilihan mobil, tolak secara halus dan arahkan kembali ke topik mobil pertama.
    """

    prompt_konteks = f"""
    [KONTEKS SIDEBAR DATA]
    - Maksimal Budget: Rp {budget_max:,}
    - Preferensi Tipe: {tipe_mobil}
    - Tujuan Penggunaan: {keperluan}

    [PERTANYAAN/PESAN PENGGUNA]
    "{pesan_user}"
    
    Berikan analisis mendalam, buatkan tabel perbandingannya, dan panggil tool pencarian jika membutuhkan referensi harga rilisan real-time di Indonesia saat ini.
    """

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.3,
        top_p=0.85,
        max_output_tokens=2500,
        tools=[cari_mobil_indonesia]
    )

    response = gemini_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt_konteks,
        config=config
    )
    return response.text

# ==============================================================================
# 4. ANTARMUKA UI STREAMLIT
# ==============================================================================
st.title("🚗 FirstCarDrive AI: Smart Recommendation Agent")
st.caption("Asisten Pintar Berbasis AI & Real-time Search untuk Memilih Mobil Pertama Anda di Indonesia")

# Sidebar untuk Input Data Terstruktur
with st.sidebar:
    st.header("📋 Kriteria Mobil Idaman")
    budget = st.slider("Maksimal Budget Anda (Rupiah):", min_value=50000000, max_value=800000000, value=200000000, step=10000000)
    
    tipe_mobil = st.selectbox(
        "Preferensi Tipe Bodi Mobil:",
        ["LCGC / City Car (Lincah & Irit)", "MPV (Keluarga & Luas)", "SUV (Tangguh & Tinggi)", "Sedan (Nyaman & Stylish)", "Bebas / Belum Tahu"]
    )
    
    keperluan = st.text_input("Tujuan Penggunaan Utama:", value="Harian Kerja & Kuliah")
    st.info("💡 Data di sidebar ini otomatis menjadi panduan awal bagi AI Agent saat Anda mengirim pesan.")

# Inisialisasi Riwayat Obrolan di Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan riwayat chat dari session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kolom Chat Input Pengguna
if user_prompt := st.chat_input("Tanyakan sesuatu tentang mobil pertama Anda di sini..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("assistant"):
        with st.spinner("FirstCarDrive AI sedang menganalisis & mencari data pasar Indonesia..."):
            try:
                jawaban_agent = jalankan_firstcar_agent(
                    budget_max=budget,
                    tipe_mobil=tipe_mobil,
                    keperluan=keperluan,
                    pesan_user=user_prompt
                )
                st.markdown(jawaban_agent)
                st.session_state.messages.append({"role": "assistant", "content": jawaban_agent})
            except Exception as e:
                # Menangkap pesan error rate limit secara spesifik
                error_msg = str(e)
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    st.warning("⚠️ **Sistem sedang sibuk (Rate Limit Gemini API tercapai).**")
                    st.info("Karena menggunakan API Free Tier, mohon tunggu sekitar 30 - 60 detik sebelum mengirimkan pesan atau pertanyaan berikutnya agar kuota di-reset kembali.")
                else:
                    st.error(f"Terjadi kesalahan sistem: {error_msg}")