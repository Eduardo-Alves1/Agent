from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from decouple import config
import pandas as pd
import os


os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')


class Agent:
    def __init__(self):
        self.__chat = ChatGroq(model= 'llama-3.1-70b-versatile', temperature=0.0 )

    def invoke(self, question, file_data):
        prompt = PromptTemplate(
            input_variables =['texto', 'dados'],
            template = ''' Você é agente que analisa informações contidas em arquivos .xlsx e .csv. Esses arquivos contem informações de monitoramento de veículos que servem para fazer gestão de frota, você terá que responder em Inglês todas as perguntas.
            <texto>
            {texto}
            dados do arquivo
            {dados}
            </texto>
            '''
        )

        chain = prompt | self.__chat | StrOutputParser()

        response = chain.invoke({
            'texto': question,
            'dados': file_data # Inicialmente, vazio para receber os dados do arquivo
        })
        return response
    
def process_file(uploaded_file):
    """Função para processar o arquivo enviado e retornar os dados em formato de string."""
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                return ("Formato de arquivo inválido. Apenas arquivos Excel (.xlsx) e CSV (.csv) são aceitos.")
                

            # Converte os dados do DataFrame em uma string
            return df.to_string(index=False)
        except Exception as e:
            print(f"Erro ao carregar a planilha: {e}")
            return None
    return None


# Função para invocar o agente
def analyze_file(mensage, file_data):
    try:
        agent = Agent()
        # Chamada para o agente
        result = agent.invoke(mensage, file_data)
        return result
    except Exception as e:
        return (f"Erro ao invocar o agente: {e}")
        