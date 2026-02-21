import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os
import re
from PIL import Image

# ==============================================================================
# 1. IDENTIDADE VISUAL & DADOS CORPORATIVOS
# ==============================================================================
COR_PRIMARIA = (0, 30, 80)      
COR_SECUNDARIA = (0, 195, 180)  
COR_FUNDO_DESTAQUE = (235, 245, 250) 

EMPRESA_NOME = "LSX MEDICAL LTDA"
EMPRESA_CNPJ = "53.210.447/0001-51"
EMPRESA_ENDERECO = "Alameda Dr. Carlos de Carvalho, 431 - 12º Andar | Curitiba - PR"
RESPONSAVEL_TECNICO = "Dra. Michelle Massaki | CRM-PR 28.435"
REGISTRO_CRM_PJ = "CRM-PR PJ 24.806"

st.set_page_config(page_title="LSX Docs Oficial", page_icon="📄", layout="wide")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #f0f2f6; }}
    .stButton > button {{
        width: 100%; border-radius: 8px; height: 3.5em; font-weight: bold; font-size: 16px;
        background-color: #001E50; color: white; border: none; transition: 0.3s;
    }}
    .stButton > button:hover {{ background-color: #00C3B4; color: white; transform: scale(1.02); }}
    h1, h2, h3, h4 {{ color: #001E50; }}
    .prompt-box {{
        background-color: #333; color: #fff; padding: 15px; border-radius: 8px; font-family: monospace;
    }}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. FUNÇÕES DE LIMPEZA E MOTOR INTELIGENTE
# ==============================================================================
def limpa_texto(texto):
    if not texto: return ""
    replacements = {"•": "-", "–": "-", "—": "-", "“": '"', "”": '"', "\u2022": "-", "\u2028": "\n"}
    for char, rep in replacements.items():
        texto = texto.replace(char, rep)
    return texto.encode('latin-1', 'replace').decode('latin-1')

def criar_marca_dagua(logo_path):
    try:
        img = Image.open(logo_path).convert("RGBA")
        fundo = Image.new('RGBA', img.size, (255, 255, 255, 255))
        img_clara = Image.blend(fundo, img, alpha=0.12) 
        img_final = img_clara.convert("RGB")
        temp_path = "temp_watermark.png"
        img_final.save(temp_path, "PNG")
        return temp_path
    except Exception as e:
        return None

def analisar_texto_inteligente(texto_bruto):
    texto_bruto = texto_bruto.replace('☑', '>>').replace('✔', '>>').replace('✓', '>>')
    blocos_pre = re.split(r'\n\s*\n', texto_bruto)
    blocos = []
    
    for bloco in blocos_pre:
        linhas = bloco.split('\n')
        bloco_atual = ""
        for linha in linhas:
            linha = linha.strip()
            if not linha: continue
            
            if not bloco_atual:
                bloco_atual = linha
            else:
                if len(bloco_atual) >= 65 and not bloco_atual.endswith(('.', ':', ';', '!', '?')):
                    bloco_atual += " " + linha
                else:
                    blocos.append(bloco_atual)
                    bloco_atual = linha
        if bloco_atual:
            blocos.append(bloco_atual)
            
    formatados = []
    for b in blocos:
        b = b.encode('latin-1', 'ignore').decode('latin-1').strip()
        if not b: continue
        
        b_lower = b.lower()
        if b_lower.startswith("base legal"):
            formatados.append(('destaque', b))
            continue
        if b.endswith(':'):
            formatados.append(('titulo_principal', b))
            continue
            
        match_bullet = re.match(r'^(\d+[\.\)]|[-*•>]+)\s*(.*)', b)
        if match_bullet:
            conteudo_sem_marcador = match_bullet.group(2)
            if len(b) < 100 and not b.endswith('.'):
                formatados.append(('subtitulo_caixa', b)) 
            else:
                formatados.append(('bullet', conteudo_sem_marcador))
        else:
            if len(b) < 80 and not b.endswith(('.', ';', ',')):
                formatados.append(('subtitulo_caixa', b)) 
            else:
                formatados.append(('paragrafo', b))
                
    return formatados

# ==============================================================================
# 3. CLASSE PDF
# ==============================================================================
class OfficialDocPDF(FPDF):
    def __init__(self, logo_path=None, watermark_path=None, tipo_documento="COMUNICADO OFICIAL", classificacao="USO INTERNO / NORMATIVO"):
        super().__init__()
        self.logo_path = logo_path
        self.watermark_path = watermark_path
        self.tipo_documento = tipo_documento
        self.classificacao = classificacao

    def header(self):
        if self.watermark_path and os.path.exists(self.watermark_path):
            self.image(self.watermark_path, x=35, y=100, w=140)

        self.set_fill_color(255, 255, 255)
        self.rect(0, 0, 210, 35, 'F')
        
        if self.logo_path and os.path.exists(self.logo_path):
            self.image(self.logo_path, x=10, y=8, w=45)
        else:
            self.set_font('Arial', 'B', 24)
            self.set_text_color(*COR_PRIMARIA)
            self.set_xy(10, 10)
            self.cell(0, 10, "LSX MEDICAL", 0, 0)

        self.set_y(10)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*COR_PRIMARIA)
        self.cell(0, 8, limpa_texto(self.tipo_documento.upper()), 0, 1, 'R')
        
        self.set_font('Arial', 'B', 9)
        self.set_text_color(*COR_SECUNDARIA)
        self.cell(0, 5, limpa_texto(self.classificacao.upper()), 0, 1, 'R')
        
        self.set_fill_color(*COR_SECUNDARIA)
        self.rect(10, 32, 190, 0.8, 'F')
        self.ln(12)

    def footer(self):
        self.set_y(-25)
        y_line = self.get_y()
        self.set_fill_color(*COR_SECUNDARIA)
        self.rect(0, y_line, 210, 1.5, 'F')
        
        self.set_y(y_line + 3)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        
        texto_rodape = f"{EMPRESA_NOME} | CNPJ: {EMPRESA_CNPJ}\n{EMPRESA_ENDERECO}\nResp. Técnico: {RESPONSAVEL_TECNICO} | {REGISTRO_CRM_PJ}"
        self.multi_cell(0, 4, limpa_texto(texto_rodape), 0, 'C')
        
        self.set_y(-12)
        self.set_font('Arial', '', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'R')

    def render_titulo_principal(self, text):
        self.ln(6)
        self.set_font('Arial', 'B', 15)
        self.set_text_color(*COR_PRIMARIA)
        self.multi_cell(0, 8, limpa_texto(text.upper()), align='L')
        self.set_fill_color(*COR_PRIMARIA)
        self.rect(10, self.get_y(), 15, 1, 'F')
        self.ln(6)

    def render_subtitulo_caixa(self, text):
        self.ln(4)
        self.set_fill_color(*COR_FUNDO_DESTAQUE)
        self.set_font('Arial', 'B', 11)
        self.set_text_color(*COR_PRIMARIA)
        y_atual = self.get_y()
        self.multi_cell(0, 8, limpa_texto("  " + text), border=0, fill=True, align='L')
        self.set_fill_color(*COR_SECUNDARIA)
        self.rect(10, y_atual, 1.5, 8, 'F') 
        self.ln(3)

    def render_paragrafo(self, text):
        self.set_font('Arial', '', 11)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 6.5, limpa_texto(text), align='J') 
        self.ln(3)

    def render_bullet(self, text):
        self.set_font('Arial', '', 11)
        self.set_text_color(60, 60, 60)
        self.set_x(15) 
        self.set_text_color(*COR_SECUNDARIA)
        self.cell(4, 6.5, chr(187), 0, 0) 
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 6.5, limpa_texto(text), align='J')
        self.ln(2)
        
    def render_destaque(self, text):
        self.set_font('Arial', 'I', 10)
        self.set_text_color(120, 120, 120) 
        self.set_x(12)
        self.multi_cell(0, 6, limpa_texto(text), align='J')
        self.ln(4)

# ==============================================================================
# 4. APP STREAMLIT (INTERFACE)
# ==============================================================================
def main():
    logo_padrao = "LOGO-LSX-Medical.png" if os.path.exists("LOGO-LSX-Medical.png") else None

    with st.sidebar:
        if logo_padrao:
            st.image(logo_padrao, width='stretch')
        st.markdown("### ⚙️ Emissor do Documento")
        nome_emissor = st.text_input("Nome", value="Rauf Alencar")
        cargo_emissor = st.text_input("Cargo", value="Gestor Comercial / Administrativo")
        st.markdown("---")
        usar_marca_dagua = st.checkbox("Incluir Marca D'água no Fundo", value=True)

    st.title("Padronizador de Documentos - LSX")
    st.markdown("Crie documentos corporativos com layout impecável.")

    col1, col2, col3 = st.columns(3)
    
    tipo_doc = col1.selectbox("Tipo de Documento", [
        "ESTRUTURA DE ATENDIMENTO",
        "COMUNICADO OFICIAL", 
        "PROCEDIMENTO OPERACIONAL (POP)",
        "CARTILHA NORMATIVA",
        "TERMO DE CONSENTIMENTO (TCLE)",
        "RELATÓRIO DE GESTÃO"
    ])
    
    classificacao_doc = col2.selectbox("Classificação (Público)", [
        "USO INTERNO / NORMATIVO",
        "USO EXTERNO / PACIENTE",
        "PÚBLICO GERAL / PARCEIROS",
        "CONFIDENCIAL / DIRETORIA"
    ])
    
    titulo_arquivo = col3.text_input("Nome do Arquivo", value="Documento_LSX")

    # --- NOVIDADE: CAIXA DE AJUDA PARA FORMATAÇÃO COM IA ---
    with st.expander("🤖 Precisa formatar um texto longo de PDF? Use este Prompt na IA:"):
        st.markdown("""
        Se o seu texto do PDF veio totalmente quebrado, copie o texto abaixo, cole no **ChatGPT, Gemini ou Claude** junto com o seu texto ruim, e cole a resposta mágica aqui no sistema:
        """)
        prompt_texto = """Atue como um revisor corporativo da LSX Medical. Seu objetivo é apenas limpar e organizar o texto abaixo para que um sistema gere um PDF padronizado.
Siga rigorosamente estas regras:
1. Junte frases quebradas ao meio (remova "Enters" indesejados).
2. Coloque o caractere de "Dois Pontos" (:) exclusivamente no final de Títulos Principais.
3. Deixe subtítulos (com ou sem números) em uma única linha curta, SEM ponto final.
4. Mantenha citações exatamente como estão, começando com "Base legal:".
Não adicione mais nada, apenas me devolva o texto limpo:

[COLE SEU TEXTO AQUI]"""
        st.code(prompt_texto, language="markdown")

    st.subheader("Conteúdo do Documento")
    texto_inserido = st.text_area(
        "Cole o texto limpo aqui", 
        height=350,
        placeholder="Lembrete: Adicione dois pontos (:) no fim de frases curtas para que virem Títulos Principais."
    )

    st.markdown("---")
    if st.button("GERAR DOCUMENTO OFICIAL (PDF) 📄"):
        if not texto_inserido.strip():
            st.warning("⚠️ Insira algum texto para gerar o documento.")
        else:
            try:
                blocos = analisar_texto_inteligente(texto_inserido)
                
                watermark_img = None
                if usar_marca_dagua and logo_padrao:
                    watermark_img = criar_marca_dagua(logo_padrao)
                
                pdf = OfficialDocPDF(logo_path=logo_padrao, watermark_path=watermark_img, tipo_documento=tipo_doc, classificacao=classificacao_doc)
                pdf.add_page()
                
                pdf.set_font('Arial', 'I', 10)
                pdf.set_text_color(120, 120, 120)
                pdf.cell(0, 6, limpa_texto(f"Emitido por: {nome_emissor} ({cargo_emissor}) - {datetime.now().strftime('%d/%m/%Y')}"), 0, 1, 'R')
                pdf.ln(5)

                for tipo, conteudo in blocos:
                    if tipo == 'titulo_principal':
                        pdf.render_titulo_principal(conteudo)
                    elif tipo == 'subtitulo_caixa':
                        pdf.render_subtitulo_caixa(conteudo)
                    elif tipo == 'bullet':
                        pdf.render_bullet(conteudo)
                    elif tipo == 'destaque':
                        pdf.render_destaque(conteudo)
                    elif tipo == 'paragrafo':
                        pdf.render_paragrafo(conteudo)

                nome_final = f"{titulo_arquivo.replace(' ', '_')}.pdf"
                pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace') 
                
                st.success("✅ Documento Padronizado com Sucesso!")
                st.download_button(
                    label="⬇️ BAIXAR DOCUMENTO (PDF)",
                    data=pdf_bytes,
                    file_name=nome_final,
                    mime="application/pdf"
                )
                
                if watermark_img and os.path.exists(watermark_img):
                    os.remove(watermark_img)

            except Exception as e:
                st.error(f"Erro ao gerar o documento: {e}")

if __name__ == "__main__":
    main()