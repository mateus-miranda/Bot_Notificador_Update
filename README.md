Bot Notificador de Atualizações do Windows para Telegram
#📖 Descrição do Projeto
Este projeto consiste em um bot em Python projetado para monitorar atualizações pendentes do sistema operacional Windows em uma ou mais máquinas. Quando atualizações são encontradas, o bot envia uma notificação detalhada e formatada para um chat específico no Telegram.

O script foi desenvolvido para ser robusto e autônomo, podendo ser compilado em um arquivo executável (.exe) e agendado para rodar periodicamente, tornando-o uma ferramenta ideal para monitoramento de máquinas de uso contínuo, como servidores ou totens de autoatendimento.

#✨ Funcionalidades Principais
Verificação de Updates: Conecta-se à API do Agente do Windows Update (WUA) para buscar atualizações de software pendentes.

Notificações Detalhadas: Envia alertas para o Telegram contendo o nome da máquina, a quantidade de atualizações e os detalhes de cada uma (Título, KB, Tamanho).

Segurança: Utiliza um arquivo .env para gerenciar segredos (Token do Bot e Chat ID), mantendo-os fora do código-fonte.

Configuração do Ambiente: Inclui funções para preparar o ambiente do Windows, desativando notificações nativas de atualização e a tela de configuração final pós-update.

Automação: Projetado para ser executado de forma autônoma através do Agendador de Tarefas do Windows.

Empacotamento: Pode ser facilmente compilado em um arquivo .exe único com o PyInstaller, eliminando a necessidade de uma instalação do Python na máquina alvo.

#🛠️ Tecnologias Utilizadas
Python 3

Bibliotecas Python:

python-telegram-bot: Para comunicação com a API do Telegram.

pywin32: Para interagir com as APIs nativas do Windows (COM e Registro).

python-dotenv: Para gerenciar variáveis de ambiente e segredos.

Ferramentas:

PyInstaller: Para empacotar o script em um executável.

Agendador de Tarefas do Windows: Para automação da execução.

#🚀 Instalação e Configuração
Siga os passos abaixo para configurar e executar o projeto em uma nova máquina.

1. Pré-requisitos
Python 3.8 ou superior.

pip (gerenciador de pacotes do Python).

2. Clonar o Repositório


git clone https://github.com/mateus-miranda/Bot_Notificador_Update.git
cd Bot_Notificador_Update

3. Configurar Ambiente Virtual (Recomendado)
É uma boa prática isolar as dependências do projeto em um ambiente virtual.

Bash

# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
No Windows:
venv\Scripts\activate

4. Instalar Dependências
Crie um arquivo chamado requirements.txt na raiz do projeto com o seguinte conteúdo:

Plaintext

# Arquivo: requirements.txt
python-telegram-bot
pywin32
python-dotenv

Em seguida, instale todas as dependências com um único comando:

pip install -r requirements.txt

5. Configurar os Segredos (.env)

Renomeie o arquivo .env.example para .env.

Abra o arquivo .env e substitua os valores de exemplo pelo seu Token do Telegram e pelo Chat ID do grupo/canal de destino.


TELEGRAM_TOKEN="SEU_TOKEN_AQUI"
TELEGRAM_CHAT_ID="SEU_CHAT_ID_AQUI"

6. Configuração Inicial do Windows (Opcional)

O script pode realizar configurações no Registro do Windows para melhorar a experiência em totens. Esta é uma ação única.

IMPORTANTE: Para que funcione, execute este comando em um terminal (CMD ou PowerShell) aberto "Como Administrador".


python main.py --configurar

Este comando irá:

Desativar as notificações de atualização que aparecem na interface do Windows.

Desativar a tela "Vamos terminar de configurar seu computador".

🏃 Uso
Para verificação normal de updates:

python main.py

Para executar a configuração inicial do sistema (requer privilégios de administrador):

python main.py --configurar

#📦 Transformando em um Executável (.exe)
Para criar um arquivo NotificadorUpdates.exe independente, utilize o PyInstaller com o seguinte comando. Ele já inclui as diretivas para lidar com a biblioteca pywin32 e para rodar de forma invisível.


pyinstaller --name "NotificadorUpdates" --onefile --windowed --hidden-import="win32com.client" --hidden-import="pythoncom" main.py

O arquivo .exe final estará na pasta dist/.

#⚙️ Automação com o Agendador de Tarefas do Windows

Para que o bot monitore a máquina de forma contínua e autônoma, agende a execução do .exe criado.

Abra o Agendador de Tarefas (taskschd.msc).

No menu "Ação", clique em "Criar Tarefa..." (não a básica).

Aba Geral:

Nome: Dê um nome claro (ex: Monitor de Updates do Telegram).

Clique em "Alterar Usuário ou Grupo...", digite SYSTEM e clique em "OK". Isso elimina a necessidade de senha.

Marque a caixa "Executar com privilégios mais altos".

Marque "Executar estando o usuário conectado ou não".

Aba Disparadores:

Clique em "Novo...".

Configure para iniciar "Diariamente" em um horário de baixa atividade (ex: 03:00).

Em "Configurações avançadas", marque "Repetir a tarefa a cada:" e defina um intervalo (ex: 6 horas) por um período "Indefinidamente".

Aba Ações:

Clique em "Novo...".

Ação: "Iniciar um programa".

Programa/script: Clique em "Procurar..." e selecione o arquivo NotificadorUpdates.exe na sua pasta dist.

Aba Condições:

Desmarque "Iniciar a tarefa somente se o computador estiver em alimentação CA" se for um notebook.

Clique em "OK" para salvar a tarefa.

#🏗️ Estrutura do Código
main.py: Arquivo principal que contém toda a lógica.

buscar_updates_windows(): Conecta-se à API do Windows para buscar atualizações pendentes.

send_message(): Função assíncrona que envia a mensagem de notificação para a API do Telegram.

desativar_notificacoes_nativas(): (Configuração) Modifica o Registro do Windows para desabilitar as notificações visuais de update.

desativar_tela_configuracao_final(): (Configuração) Modifica o Registro para desabilitar a tela de configuração pós-update.

main(): Função principal que orquestra a execução, decidindo se roda em modo "verificação" ou "configuração" e construindo a mensagem de alerta.

