import streamlit as st
import discord
import asyncio
# A biblioteca commands não é estritamente necessária para usar discord.Client, 
# mas mantivemos caso você queira expandir no futuro.
from discord.ext import commands 

# --- CONFIGURAÇÃO DE SEGREDOS ---
# Procura o token no arquivo .streamlit/secrets.toml
try:
    DISCORD_BOT_TOKEN = st.secrets["discord"]["token"]
except (FileNotFoundError, KeyError):
    # Se o arquivo não existir ou a chave estiver errada
    DISCORD_BOT_TOKEN = None

# Configurar as Intents
intents = discord.Intents.default()

# --- FUNÇÃO PRINCIPAL DE CONSULTA ---
async def fetch_discord_user(user_id: int):
    """
    Função assíncrona que inicializa um cliente Discord para buscar um usuário por ID.
    """
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        pass 

    try:
        # Tenta conectar e rodar o cliente
        await client.login(DISCORD_BOT_TOKEN)
        
        # Tenta buscar o usuário
        user = await client.fetch_user(user_id)
        
        await client.close()
        return user

    except discord.NotFound:
        await client.close()
        return "Not Found"
    except discord.errors.LoginFailure:
        await client.close()
        return "Invalid Token"
    except Exception as e:
        await client.close()
        return f"Error: {e}"


# --- INTERFACE STREAMLIT ---

st.title("🔎 Discord ID para Nome de Usuário")
st.markdown("Insira um ID numérico do Discord para obter o nome de usuário.")

# VERIFICAÇÃO DE SEGURANÇA DO TOKEN
if DISCORD_BOT_TOKEN is None:
    st.error("🔒 **Erro de Configuração:**")
    st.markdown("""
    O Token do Discord não foi encontrado. Crie um arquivo chamado `.streamlit/secrets.toml` na pasta do projeto com o seguinte conteúdo:
    ```toml
    [discord]
    token = "SEU_TOKEN_AQUI"
    ```
    """)
    st.stop() # Para a execução do script aqui até que o erro seja resolvido

st.info("Lembre-se de ativar o **Server Members Intent** no Portal do Desenvolvedor!")

# Campo de entrada
input_id = st.text_input("Insira o Discord ID (Ex: 123456789012345678)", max_chars=20)

# Botão de busca
if st.button("Buscar Usuário"):
    
    # 1. Validação do Input
    if not input_id.strip().isdigit():
        st.error("Por favor, insira apenas números válidos.")
    else:
        # 2. Execução da busca
        with st.spinner('Buscando na API do Discord...'):
            try:
                # Executa a função assíncrona
                user_result = asyncio.run(fetch_discord_user(int(input_id)))

                # 3. Processamento do Resultado
                if user_result == "Not Found":
                    st.warning(f"❌ Não foi possível encontrar um usuário com o ID: `{input_id}`")
                elif user_result == "Invalid Token":
                    st.error("🚨 Erro de Autenticação: O Token no secrets.toml parece inválido.")
                elif isinstance(user_result, str) and user_result.startswith("Error:"):
                    st.error(f"❌ Ocorreu um erro técnico: {user_result}")
                else:
                    # Sucesso
                    st.success("✅ Usuário Encontrado!")
                    
                    # Exibe os dados formatados
                    st.json({
                        "ID": str(user_result.id), # Convertido para string para garantir visualização correta
                        "Username": user_result.name,
                        "Global Name": user_result.global_name if user_result.global_name else "N/A",
                        "Creation Date": user_result.created_at.strftime("%d/%m/%Y %H:%M:%S UTC"),
                        "Avatar URL": str(user_result.avatar.url) if user_result.avatar else "Sem Avatar"
                    })
                    
                    # Se tiver avatar, mostra a imagem
                    if user_result.avatar:
                        st.image(user_result.avatar.url, width=100, caption=user_result.name)
                    
            except ValueError:
                 st.error("O ID inserido é muito grande ou inválido.")
            except Exception as e:
                st.error(f"Ocorreu um erro fatal: {e}")