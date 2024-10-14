import streamlit as st
from ia.cliente import analyze_file, process_file

st.image("image/pngegg.png", width= 100)
# Aplicação Streamlit
st.title("Análise de Veículos")

st.subheader("Selecione a planilha")
uploaded_file = st.file_uploader("Carregar Planilha", type=["xlsx", "csv"])

mensage = st.chat_input(placeholder='Perguntar')

# Verifica se o botão foi clicado
if mensage:
    if uploaded_file is None:
        st.error("Por favor, carregue uma planilha.")
    elif not mensage:
        st.error("Por favor, insira uma pergunta para a análise.")
    else:
        # Processa o arquivo
        file_data = process_file(uploaded_file)
        if file_data:
            st.write("Dados do arquivo processados com sucesso.")
            result = analyze_file(mensage, file_data)
            if result is not None:
                
                st.markdown(''' :green[**Resposta AI:** ] ''')
                st.write(f":robot_face:  {result}")
        else:
            st.error("Erro ao processar o arquivo.")
