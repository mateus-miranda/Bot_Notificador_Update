import asyncio
import telegram
import win32com.client
import pythoncom
import socket # Import para pegar o Hostname
#Import para tentar desativar as notificacoes
import winreg
import ctypes
import sys

# --- CONFIGURAÇÃO ---
TOKEN = "7980162914:AAFoK_YwqY4YqvUy7TSbX_7WCfXwcWkw-Qk"
CHAT_ID = "-1002836339711"
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

# --- FUNÇÃO 2:
async def send_message(text, chat_id, parse_mode=None):
    """Envia uma mensagem para o Telegram."""
    async with bot:
        await bot.send_message(text=text, chat_id=chat_id, parse_mode=parse_mode)

# --- FUNÇÃO 3:
def desativar_notificacoes_nativas():
    """
    Tenta desativar as notificações de UI do Windows Update via Registro.
    Requer privilégios de Administrador para funcionar.
    """
    try:
        # 1. Verifica se o script está rodando como Administrador
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if not is_admin:
            print("AVISO: Para desativar as notificações, o script precisa ser executado como Administrador.")
            return False

        # 2. Caminho e chave do registro para desativar as notificações da UI
        registry_path = r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate"
        key_name = "SetDisableUXWUAccess"
        key_value = 1
        
        print("Tentando desativar as notificações nativas do Windows Update...")
        # 3. Abre (ou cria) a chave principal
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, registry_path)
        
        # 4. Define o valor que desativa a notificação
        winreg.SetValueEx(key, key_name, 0, winreg.REG_DWORD, key_value)
        
        # 5. Fecha a chave do registro
        winreg.CloseKey(key)
        
        print("SUCESSO: As notificações nativas do Windows Update foram desativadas.")
        return True

    except PermissionError:
        print("ERRO: Permissão negada. Execute o script como Administrador para alterar o registro.")
        return False
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao tentar modificar o registro: {e}")
        return False
    
# --- FUNÇÃO 4:
def desativar_tela_configuracao_final():
    """
    Desativa a tela "Vamos terminar de configurar seu computador" que aparece
    após algumas atualizações do Windows.
    """
    try:
        print("Tentando desativar a tela de configuração final do Windows...")
        # Caminho no registro do usuário atual
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager"
        key_name = "SubscribedContent-310760Enabled"
        key_value = 0 # 0 para desativado

        # Abre a chave do registro
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE)

        # Define o valor que desativa a tela
        winreg.SetValueEx(key, key_name, 0, winreg.REG_DWORD, key_value)

        # Fecha a chave
        winreg.CloseKey(key)
        print("SUCESSO: Tela de configuração final foi desativada.")
        return True
    except FileNotFoundError:
        print("AVISO: A chave de registro para desativar a tela de configuração não foi encontrada. Pode não ser necessário nesta versão do Windows.")
        return False
    except Exception as e:
        print(f"ERRO ao tentar desativar a tela de configuração: {e}")
        return False

# --- FUNÇÃO 5:
async def main():
    """Função principal que executa a lógica do bot."""
    desativar_notificacoes_nativas()
    desativar_tela_configuracao_final()

    print("Iniciando verificação...")
    lista_de_updates = buscar_updates_windows()

    if lista_de_updates:
        hostname = socket.gethostname()

        # Insere a variável 'hostname' no título da mensagem
        mensagem = f"*Alerta de Updates na Máquina: {hostname}*\n\n" 
        mensagem += f"Foram encontradas *{len(lista_de_updates)}* atualizações pendentes:\n--------------------------------------\n\n"

        for update in lista_de_updates:
            mensagem += f"*{update['Titulo']}*\n  KB: {update['KB']}\n  Tamanho: {update['Tamanho_MB']:.2f} MB\n\n"
        
        print("Enviando notificação para o Telegram...")
        await send_message(text=mensagem, chat_id=CHAT_ID, parse_mode='Markdown')
        print("Notificação enviada!")
    else:
        print("Nenhuma atualização pendente encontrada.")

# --- PONTO DE ENTRADA ---
if __name__ == '__main__':
    asyncio.run(main())