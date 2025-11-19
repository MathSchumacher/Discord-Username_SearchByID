import streamlit as st
import discord
import asyncio
import time
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Discord ID Resolver Pro",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS AVANÇADO (VISUAL PROFESSIONAL) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* 1. Fundo Radial (O que você gostou) */
    .stApp {
        background-color: #0e1015;
        background-image: radial-gradient(circle at 50% 0%, #1e212b 0%, #0e1015 70%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* 2. Títulos (Gradiente Roxo/Azul) */
    h1 {
        font-weight: 800 !important;
        background: linear-gradient(90deg, #5865F2, #9B84EC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .subtitle {
        color: #b9bbbe;
        font-size: 0.95rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* 3. A "Caixa 3D" (Instruções) - Efeito Neumórfico Real */
    /* Isso substitui a caixa preta vazia por algo que parece sair da tela */
    .neumorphic-box {
        background: #131519;
        border-radius: 12px;
        /* O segredo do 3D: Sombra escura de um lado, clara do outro */
        box-shadow:  7px 7px 14px #0a0b0d, 
                    -7px -7px 14px #1c1f25;
        padding: 20px;
        text-align: center;
        color: #949BA4;
        font-size: 0.9rem;
        border: 1px solid rgba(255,255,255,0.02);
        margin-bottom: 30px;
    }

    /* 4. Input Field (Correção do Hover "Estranho") */
    /* Base */
    .stTextArea textarea {
        background-color: #0a0a0a !important; /* Contraste forte */
        color: #ffffff !important;
        border: 2px solid #2f3136 !important; /* Borda cinza sólida inicial */
        border-radius: 12px !important;
        font-family: 'Consolas', monospace;
        transition: all 0.4s ease-in-out; /* Transição lenta e suave */
    }

    /* Foco - Animação Profissional */
    .stTextArea textarea:focus {
        /* Borda vira roxa sólida para combinar com o título */
        border-color: #5865F2 !important; 
        /* Um brilho (Glow) difuso e elegante */
        box-shadow: 0 0 25px rgba(88, 101, 242, 0.35) !important; 
        /* Leve aumento de escala */
        transform: scale(1.01);
        background-color: #101014 !important;
    }

    /* 5. Card Principal (Glassmorphism sutil para segurar o layout) */
    .glass-container {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 30px;
    }

    /* 6. Botão (Melhorado e Alinhado) */
    .stButton > button {
        background: linear-gradient(90deg, #5865F2, #9B84EC); /* Mesmo gradiente do título */
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        height: 50px; /* Altura fixa */
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        margin-top: 27px; /* Alinhamento milimétrico com o input */
        box-shadow: 0 4px 15px rgba(88, 101, 242, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(155, 132, 236, 0.5);
    }
    .stButton > button:active {
        transform: scale(0.98);
    }

    /* Remove padding extra do topo do Streamlit */
    .block-container { padding-top: 2rem; }

</style>
""", unsafe_allow_html=True)

# --- LÓGICA BACKEND ---
async def fetch_user_data_with_delay(user_id: int, token: str, delay_sec: float = 0.2):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    try:
        await client.login(token)
        user = await client.fetch_user(user_id)
        return {
            "id": str(user.id),
            "username": user.name,
            "global_name": user.global_name if user.global_name else "-",
            "created_at_fmt": user.created_at.strftime("%d/%m/%Y"),
            "avatar_url": user.avatar.url if user.avatar else "https://cdn.discordapp.com/embed/avatars/0.png",
            "status": "success"
        }
    except discord.NotFound:
        return {"id": str(user_id), "username": "N/A", "status": "not_found", "avatar_url": None}
    except Exception:
        return {"id": str(user_id), "username": "Erro", "status": "error", "avatar_url": None}
    finally:
        await asyncio.sleep(delay_sec)
        await client.close()

# --- INTERFACE ---

# Header
st.markdown("<h1>⚡ Discord ID Resolver</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Converta IDs brutos em identidades reais. Rápido. Seguro. Ilimitado.</p>', unsafe_allow_html=True)

# A CAIXA 3D NEUMÓRFICA (Preenche o espaço vazio com estilo)
st.markdown("""
    <div class="neumorphic-box">
        <strong>SISTEMA PRONTO.</strong><br>
        <span style="opacity: 0.7;">Cole os IDs abaixo. O sistema limpa espaços e textos inválidos automaticamente.</span>
    </div>
""", unsafe_allow_html=True)

# Container Principal
with st.container():
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    # Layout [3, 1]
    col_input, col_btn = st.columns([3, 1], gap="medium")
    
    with col_input:
        st.markdown("### 📥 Target List")
        raw_input = st.text_area(
            "label_oculta", # Label necessária para acessibilidade, mas oculta visualmente
            height=150, 
            placeholder="262745192195624256\n8923472384423894\n...",
            label_visibility="collapsed"
        )
        
    with col_btn:
        # Botão alinhado
        run_btn = st.button("INICIAR")
        
        st.markdown("""
            <div style="text-align: center; margin-top: 10px; opacity: 0.5; font-size: 10px;">
                SAFE RATE LIMIT
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- EXECUÇÃO ---
if run_btn:
    try:
        BOT_TOKEN = st.secrets["discord"]["token"]
    except:
        st.error("Erro: Token não encontrado em .streamlit/secrets.toml")
        st.stop()

    if not raw_input.strip():
        st.warning("⚠️ Lista vazia.")
    else:
        id_list = [line.strip() for line in raw_input.split('\n') if line.strip().isdigit()]
        
        if not id_list:
            st.error("❌ Nenhum ID válido encontrado.")
        else:
            # Progresso
            st.markdown("---")
            status_placeholder = st.empty()
            bar = st.progress(0)
            
            results = []
            for i, uid in enumerate(id_list):
                status_placeholder.markdown(f"**Analisando:** `{uid}`")
                data = asyncio.run(fetch_user_data_with_delay(int(uid), BOT_TOKEN))
                results.append(data)
                bar.progress((i + 1) / len(id_list))
            
            status_placeholder.empty()
            bar.empty()

            # Tabela
            df = pd.DataFrame(results)
            
            st.dataframe(
                df,
                column_config={
                    "avatar_url": st.column_config.ImageColumn("Avatar", width="small"),
                    "username": st.column_config.TextColumn("User", width="medium"),
                    "id": st.column_config.TextColumn("ID", width="medium"),
                    "created_at_fmt": st.column_config.TextColumn("Data", width="small"),
                    "global_name": st.column_config.TextColumn("Display Name", width="medium"),
                    "status": st.column_config.TextColumn("Status", width="small"),
                },
                column_order=["avatar_url", "username", "id", "created_at_fmt", "global_name"],
                use_container_width=True,
                hide_index=True
            )

            # Download Button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 BAIXAR CSV",
                data=csv,
                file_name=f"discord_export_{datetime.now().strftime('%H%M')}.csv",
                mime='text/csv'
            )

# Footer
st.markdown("""
<div style="margin-top: 40px; text-align: center; opacity: 0.3; font-size: 11px;">
    POWERED BY STREAMLIT & DISCORD API
</div>
""", unsafe_allow_html=True)