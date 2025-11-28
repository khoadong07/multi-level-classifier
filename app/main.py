"""Streamlit UI for SPX Classification System - Centralized Architecture"""
import streamlit as st
from pathlib import Path

from .core import Config, Classifier, CacheManager, CentralProcessor
from .utils import to_excel_bytes


# ========================= PAGE CONFIGURATION =========================
st.set_page_config(layout="wide", page_title="AI Feedback Classification Tool")
st.title("🤖 AI SPX Classification Tool")
st.subheader("Hệ thống phân loại feedback khách hàng sử dụng LLM - Kiến trúc tập trung")


# ========================= INITIALIZATION =========================
@st.cache_resource
def initialize_system():
    """Initialize the classification system components"""
    try:
        Config.validate()
        prompt_template = Config.load_prompt_template()
        
        classifier = Classifier(
            base_url=Config.OPENAI_BASE_URL,
            api_key=Config.OPENAI_API_KEY,
            model=Config.MODEL,
            prompt_template=prompt_template,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS
        )
        
        cache_manager = CacheManager(Config.CACHE_FILE)
        
        processor = CentralProcessor(
            classifier=classifier,
            cache_manager=cache_manager,
            max_workers=Config.MAX_WORKERS
        )
        
        return processor, cache_manager
    
    except Exception as e:
        st.error(f"Lỗi khởi tạo hệ thống: {e}")
        st.stop()


processor, cache_manager = initialize_system()


# ========================= SESSION STATE =========================
if 'df_input' not in st.session_state:
    st.session_state.df_input = None
if 'df_output' not in st.session_state:
    st.session_state.df_output = None
if 'uploaded_filename' not in st.session_state:
    st.session_state.uploaded_filename = None


# ========================= SIDEBAR =========================
st.sidebar.header("⚙️ Cấu hình hệ thống")

# System info
st.sidebar.markdown(f"**Model:** `{Config.MODEL}`")
st.sidebar.markdown(f"**Base URL:** `{Config.OPENAI_BASE_URL}`")
st.sidebar.markdown(f"**Max Workers:** `{Config.MAX_WORKERS}`")
st.sidebar.markdown(f"**Cache Size:** `{len(cache_manager.cache)} entries`")

# File upload
uploaded_file = st.sidebar.file_uploader(
    "1. Tải lên file Excel (.xlsx)",
    type=["xlsx"],
    help="File phải chứa các cột: 'Title', 'Content', 'Description'"
)

st.sidebar.markdown("---")
st.sidebar.markdown("v2.0 - Kiến trúc tập trung - Nov 2025")

# Load uploaded file
if uploaded_file is not None:
    try:
        if (st.session_state.df_input is None or 
            uploaded_file.name != st.session_state.uploaded_filename):
            
            from .utils import load_excel
            df = load_excel(uploaded_file)
            st.session_state.df_input = df
            st.session_state.df_output = None
            st.session_state.uploaded_filename = uploaded_file.name
            st.sidebar.success(f"✅ Đã tải file: {len(df)} dòng")
    
    except Exception as e:
        st.sidebar.error(f"❌ Lỗi đọc file: {e}")
        st.session_state.df_input = None


# ========================= MAIN INTERFACE =========================

# --- 1. Data Preview ---
st.header("1. Xem trước dữ liệu")
if st.session_state.df_input is not None:
    st.info(f"Hiển thị 10 dòng đầu tiên (Tổng: {len(st.session_state.df_input)} dòng)")
    st.dataframe(st.session_state.df_input.head(10), use_container_width=True)
else:
    st.warning("👈 Vui lòng tải lên file Excel ở sidebar")


# --- 2. Classification Execution ---
st.header("2. Thực hiện phân loại")

col1, col2 = st.columns([3, 1])
with col1:
    clear_cache = st.checkbox(
        "Xóa cache trước khi chạy",
        value=False,
        help="Xóa tất cả kết quả đã lưu trong cache"
    )

with col2:
    execute_button = st.button(
        "🚀 Bắt đầu phân loại",
        disabled=st.session_state.df_input is None,
        use_container_width=True
    )

if execute_button:
    if clear_cache:
        cache_manager.clear()
        st.success("✅ Đã xóa cache")
    
    df = st.session_state.df_input
    
    # Prepare tasks
    with st.spinner("Đang chuẩn bị tasks..."):
        tasks = processor.prepare_tasks(df)
    
    if not tasks:
        st.warning("⚠️ Không tìm thấy feedback hợp lệ để phân loại")
        st.stop()
    
    st.info(f"📊 Đã chuẩn bị {len(tasks)} tasks với {Config.MAX_WORKERS} workers")
    
    # Progress tracking
    progress_bar = st.progress(0, text="Đang xử lý...")
    status_container = st.empty()
    
    def update_progress(completed: int, total: int):
        """Callback to update progress"""
        percent = completed / total
        progress_bar.progress(percent, text=f"Đang xử lý: {completed}/{total} ({percent*100:.1f}%)")
    
    # Process batch
    results, stats = processor.process_batch(tasks, progress_callback=update_progress)
    
    # Apply results to DataFrame
    df_output = processor.apply_results_to_dataframe(df, results)
    st.session_state.df_output = df_output
    
    # Clear progress
    progress_bar.empty()
    
    # Show statistics
    st.success("✅ Hoàn thành phân loại!")
    
    st.markdown("---")
    st.header("3. Thống kê kết quả")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng số dòng", stats.total_tasks)
    col2.metric("Cache hits", stats.cache_hits, help="Số lượng kết quả lấy từ cache")
    col3.metric("API calls", stats.api_calls, help="Số lượng gọi API mới")
    col4.metric("Thất bại", stats.failed, help="Số lượng phân loại thất bại")
    
    # Calculate success rate
    success_rate = ((stats.cache_hits + stats.api_calls) / stats.total_tasks * 100) if stats.total_tasks > 0 else 0
    st.metric("Tỷ lệ thành công", f"{success_rate:.1f}%")
    
    st.markdown("---")


# --- 4. Download & Preview ---
if st.session_state.df_output is not None and "label_en" in st.session_state.df_output.columns:
    st.header("4. Tải xuống kết quả")
    
    # Generate Excel bytes
    excel_bytes = to_excel_bytes(st.session_state.df_output)
    
    # Determine filename
    output_filename = "classified_output.xlsx"
    if st.session_state.uploaded_filename:
        base_name = Path(st.session_state.uploaded_filename).stem
        output_filename = f"{base_name}_classified.xlsx"
    
    st.download_button(
        label="📥 Tải xuống file Excel đã phân loại",
        data=excel_bytes,
        file_name=output_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
    
    st.markdown("---")
    st.subheader("Xem trước kết quả (10 dòng đầu)")
    
    # Highlight classification columns
    highlight_cols = ["label_en", "label_1", "label_2", "label_3", "label_4"]
    
    def highlight_new_cols(s):
        return ['background-color: #a10239' if s.name in highlight_cols else '' for _ in s]
    
    styler = st.session_state.df_output.head(10).style.apply(highlight_new_cols, axis=0)
    st.dataframe(styler, use_container_width=True)


# ========================= FOOTER =========================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>SPX Classification System v2.0 - Centralized Processing Architecture</p>
    <p>Powered by LLM | Built with Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
