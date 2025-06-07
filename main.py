import asyncio
import telegram
import win32com.client
import pythoncom
import os  # <--- 1. Importar a biblioteca 'os'
from dotenv import load_dotenv  # <--- 2. Importar a função 'load_dotenv'

# --- CONFIGURAÇÃO ---
load_dotenv()  # <--- 3. Carrega as variáveis do arquivo .env

# 4. Lê as variáveis do ambiente
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Verifica se as variáveis foram carregadas
if not TOKEN or not CHAT_ID:
    raise ValueError("As variáveis de ambiente TELEGRAM_TOKEN e TELEGRAM_CHAT_ID não foram definidas!")

bot = telegram.Bot(token=TOKEN)

# --- FUNÇÃO 1:
def buscar_updates_windows():
    """Busca por atualizações do Windows e retorna uma lista com detalhes."""
    pythoncom.CoInitialize()
    try:
        update_session = win32com.client.Dispatch("Microsoft.Update.Session")
        update_searcher = update_session.CreateUpdateSearcher()
        search_result = update_searcher.Search("IsInstalled=0 and Type='Software'")
        
        if search_result.Updates.Count == 0:
            return []

        updates_encontrados = []
        for update in search_result.Updates:
            updates_encontrados.append({
                "Titulo": update.Title,
                "KB": ", ".join(kb for kb in update.KBArticleIDs) if update.KBArticleIDs else "N/A",
                "Tamanho_MB": int(update.MaxDownloadSize) / (1024 * 1024) if hasattr(update, "MaxDownloadSize") else 0
            })
        return updates_encontrados
    except Exception as e:
        print(f"Ocorreu um erro ao buscar atualizações: {e}")
        return []
    finally:
        pythoncom.CoUninitialize()

# --- FUNÇÃO 2: A VOZ ---
async def send_message(text, chat_id, parse_mode=None):
    """Envia uma mensagem para o Telegram."""
    async with bot:
        await bot.send_message(text=text, chat_id=chat_id, parse_mode=parse_mode)

# --- FUNÇÃO 3: O ORQUESTRADOR ---
async def main():
    """Função principal que executa a lógica do bot."""
    print("Iniciando verificação...")
    lista_de_updates = buscar_updates_windows()

    if lista_de_updates:
        mensagem = f" *Alerta de Atualizações do Windows!*\n\nForam encontradas *{len(lista_de_updates)}* atualizações pendentes:\n--------------------------------------\n\n"
        for update in lista_de_updates:
            mensagem += f"*{update['Titulo']}*\n  KB: {update['KB']}\n  Tamanho: {update['Tamanho_MB']:.2f} MB\n\n"
        
        print("Enviando notificação para o Telegram...")
        await send_message(text=mensagem, chat_id=CHAT_ID, parse_mode='Markdown')
        print("Notificação enviada!")
    else:
        print("Nenhuma atualização pendente encontrada.")

        #mensagem_ok = "Verificação concluída. Nenhuma atualização disponivel"
        #await send_message(text=mensagem_ok, chat_id=CHAT_ID)
        #print("Enviada mensagem de 'status OK' para o Telegram.")

# --- PONTO DE ENTRADA ---
if __name__ == '__main__':
    asyncio.run(main())