import json
import urllib.parse
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Orçamento - Oficina de Celulares", page_icon="📱", layout="centered"
)

st.title("📱 Simulador de Orçamento de Reparo")
st.write(
    "Selecione o tipo de peça, o modelo do seu smartphone e veja a estimativa"
    " de valores."
)

# Carregar os dados de preços do arquivo precos.json
try:
  with open("precos.json", "r", encoding="utf-8") as f:
    tabela_precos = json.load(f)
except FileNotFoundError:
  st.error(
      "Arquivo 'precos.json' não encontrado. Certifique-se de salvá-lo na mesma"
      " pasta."
  )
  st.stop()

# Dicionário com as taxas fixas por categoria (já embutindo mão de obra + frete)
taxas_servico = {
    "telas": 215.0,
    "placas_de_carga": 95.0,
    "tampas": 50.0,
    "baterias": 50.0,
}

# 1. O cliente seleciona o serviço (Categoria)
categorias_disponiveis = list(tabela_precos.keys())
categoria_escolhida = st.selectbox(
    "Selecione o Tipo de Serviço / Componente:", options=categorias_disponiveis
)

# Obter lista de modelos para a categoria selecionada
itens_categoria = tabela_precos[categoria_escolhida]

# Se a categoria for "telas", filtramos removendo os modelos "incell" ou "incel"
if categoria_escolhida == "telas":
  itens_filtrados = [
      item
      for item in itens_categoria
      if "incell" not in item["modelo"].lower()
      and "incel" not in item["modelo"].lower()
  ]
else:
  itens_filtrados = itens_categoria

mapa_modelos = {item["modelo"]: item["preco"] for item in itens_filtrados}

# 2. O cliente seleciona o modelo do celular
modelo_selecionado = st.selectbox(
    "Selecione o Modelo do Aparelho:", options=list(mapa_modelos.keys())
)

# Recuperar o valor da peça e somar a taxa correspondente de forma oculta nos bastidores
preco_peca = mapa_modelos[modelo_selecionado]
taxa_aplicada = taxas_servico.get(categoria_escolhida, 0.0)
preco_total = preco_peca + taxa_aplicada

st.divider()
st.subheader("🛠️ Resumo do Orçamento:")

nome_servico_formatado = categoria_escolhida.replace("_", " ").title()

st.write(f"**Serviço:** {nome_servico_formatado}")
st.write(f"**Modelo:** {modelo_selecionado}")

st.divider()

# Exibição do Valor Total Final unificado
st.markdown(f"### **Valor Total Estimado: R$ {preco_total:.2f}**")

st.info(
    "💡 *Trabalhamos sob encomenda. O valor total já inclui o componente e a"
    " execução do serviço.*"
)

# 3. Mensagem para o WhatsApp (com o valor total fechado)
texto_whatsapp = (
    f"Olá! Fiz uma simulação no site para o serviço de"
    f" *{nome_servico_formatado}* no modelo *{modelo_selecionado}* (Valor"
    f" Total Estimado: R$ {preco_total:.2f}). Como vocês trabalham sob"
    f" encomenda, gostaria de confirmar a disponibilidade e como faço para"
    f" encomendar a peça."
)

texto_encoded = urllib.parse.quote(texto_whatsapp)
# Substitua pelo seu número correto com DDI e DDD
url_zap = f"https://wa.me/5551996210611?text={texto_encoded}"

st.markdown(
    f'<a href="{url_zap}" target="_blank"><button style="background-color:#25D366;'
    " color:white; padding:12px 24px; border:none; border-radius:5px;"
    " font-weight:bold; cursor:pointer; font-size:16px;"
    ' width:100%;">📲 Encomendar Peça / Fechar via WhatsApp</button></a>',
    unsafe_allow_html=True,
)