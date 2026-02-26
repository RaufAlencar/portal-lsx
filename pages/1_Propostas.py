import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os

# ==============================================================================
# 1. IDENTIDADE VISUAL & DADOS CORPORATIVOS (LSX MEDICAL)
# ==============================================================================
COR_PRIMARIA = (0, 30, 80)      # Azul Navy Profundo (LSX Dark)
COR_SECUNDARIA = (0, 195, 180)  # Turquesa/Ciano Vibrante (LSX Highlight)
COR_CINZA_CLARO = (245, 246, 250)

# Dados Institucionais e Legais
EMPRESA_NOME = "LSX MEDICAL LTDA"
EMPRESA_CNPJ = "53.210.447/0001-51"
EMPRESA_ENDERECO = "Alameda Dr. Carlos de Carvalho, 431 - 12º Andar | Curitiba - PR"
EMPRESA_SITE = "www.lsxmedical.com.br"
RESPONSAVEL_TECNICO = "Dra. Michelle Massaki | CRM-PR 28.435"
REGISTRO_CRM_PJ = "CRM-PR PJ 24.806"

st.set_page_config(page_title="LSX Propostas", page_icon="✚", layout="wide")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #f0f2f6; }}
    .stButton > button {{
        width: 100%; border-radius: 8px; height: 3.5em; font-weight: bold; font-size: 16px;
        background-color: #001E50; color: white; border: none; transition: 0.3s;
    }}
    .stButton > button:hover {{ background-color: #00C3B4; color: white; transform: scale(1.02); }}
    h1, h2, h3, h4 {{ color: #001E50; }}
    .highlight-box {{
        background-color: #E0F7FA; padding: 20px; border-radius: 10px; 
        border-left: 6px solid #00C3B4; margin-bottom: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# Limpeza de caracteres não suportados pelo FPDF
def limpa_texto(texto):
    if not texto: return ""
    replacements = {"•": "-", "–": "-", "—": "-", "“": '"', "”": '"', "\u2022": "-", "\u2028": "\n"}
    for char, rep in replacements.items():
        texto = str(texto).replace(char, rep)
    return texto.encode('latin-1', 'replace').decode('latin-1')

# ==============================================================================
# 2. MOTOR DE PRECIFICAÇÃO DINÂMICA
# ==============================================================================
def calcular_preco_sugerido(vidas):
    if vidas <= 0: return 0.00
    if vidas <= 200: return 7.90
    if vidas <= 999: return 6.90
    if vidas <= 2999: return 5.90
    if vidas <= 5999: return 5.49
    if vidas <= 8999: return 4.90
    if vidas <= 11999: return 4.49
    if vidas <= 14999: return 3.90
    if vidas <= 17999: return 3.49
    if vidas <= 20999: return 2.90
    if vidas <= 23999: return 2.49
    if vidas <= 26999: return 1.90
    if vidas <= 29999: return 1.49
    return 0.90

# ==============================================================================
# 3. CLASSE PDF PROFISSIONAL (GERADOR DE RELATÓRIO)
# ==============================================================================
class ProposalPDF(FPDF):
    def __init__(self, logo_path=None):
        super().__init__()
        self.logo_path = logo_path

    def header(self):
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
        self.set_font('Arial', 'B', 15)
        self.set_text_color(*COR_PRIMARIA)
        self.cell(0, 8, 'PROPOSTA COMERCIAL', 0, 1, 'R')
        
        self.set_font('Arial', 'B', 9)
        self.set_text_color(*COR_SECUNDARIA)
        self.cell(0, 5, limpa_texto('SUA MARCA, NOSSA TECNOLOGIA.'), 0, 1, 'R')
        
        self.set_fill_color(*COR_SECUNDARIA)
        self.rect(10, 32, 190, 0.8, 'F')
        self.ln(12)

    def footer(self):
        self.set_y(-28)
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

    def chapter_title(self, title):
        self.ln(5)
        self.set_font('Arial', 'B', 13)
        self.set_text_color(*COR_PRIMARIA)
        self.cell(0, 8, limpa_texto(title.upper()), 0, 1, 'L')
        self.set_fill_color(*COR_PRIMARIA)
        self.rect(10, self.get_y(), 10, 0.8, 'F')
        self.ln(5)

    def sub_title(self, title):
        self.set_font('Arial', 'B', 11)
        self.set_text_color(*COR_PRIMARIA)
        self.cell(0, 6, limpa_texto(title), 0, 1, 'L')
        self.ln(1)

    def body_text(self, text):
        self.set_font('Arial', '', 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5, limpa_texto(text), align='J')
        self.ln(3)

    def bullet_point(self, text):
        self.set_font('Arial', '', 10)
        self.set_text_color(50, 50, 50)
        self.cell(5) 
        self.set_text_color(*COR_SECUNDARIA)
        self.cell(3, 5, "»", 0, 0) 
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5, limpa_texto(text), align='J')
        self.ln(1)

# ==============================================================================
# 4. APP STREAMLIT (LÓGICA E INTERFACE)
# ==============================================================================
def main():
    logo_padrao = "LOGO-LSX-Medical.png" if os.path.exists("LOGO-LSX-Medical.png") else None

    # --- SIDEBAR ---
    with st.sidebar:
        if logo_padrao:
            st.image(logo_padrao, width='stretch')
        else:
            st.title("LSX Config")
            
        st.markdown("### 👤 Dados do Emissor")
        nome_vendedor = st.text_input("Nome", value="")
        cargo_vendedor = st.text_input("Cargo", value="")
        telefone_vendedor = st.text_input("Telefone", value="")
        email_vendedor = st.text_input("E-mail", value="@lsxmedical.com")
        
        st.markdown("---")
        st.markdown("### ⚙️ Configurações Visuais")
        uploaded_logo = st.file_uploader("Trocar Logo LSX (Opcional)", type=['png', 'jpg'])
        if uploaded_logo:
            with open("temp_logo.png", "wb") as f:
                f.write(uploaded_logo.getbuffer())
            logo_final = "temp_logo.png"
        else:
            logo_final = logo_padrao

    # --- MAIN CONTENT ---
    st.title("Gerador de Propostas Enterprise - LSX Medical")
    st.markdown("Plataforma White Label B2B - Configuração de Contratos Avançados")

    # SEÇÃO 1: CLIENTE
    st.subheader("1. Dados do Cliente (Contratante)")
    col1, col2 = st.columns(2)
    cliente_empresa = col1.text_input("Razão Social / Empresa", placeholder="Ex: Grupo UMUPREV")
    cliente_responsavel = col2.text_input("Nome do Responsável", placeholder="Ex: João Silva")
    
    nome_fantasia_cliente = cliente_empresa if cliente_empresa else "Sua Empresa"

    st.markdown("---")
    
    # SEÇÃO 2: PRECIFICAÇÃO (SIMPLES OU RAMPA)
    st.subheader("2. Dimensionamento e Precificação")
    
    usar_rampa = st.checkbox("📈 Habilitar Rampa de Lançamento (Contrato com Escalonamento Mensal)")
    
    dados_rampa = None # Variável para armazenar a tabela se existir
    
    if usar_rampa:
        st.info("Preencha a tabela abaixo com a projeção mês a mês. O PDF gerará um cronograma financeiro completo.")
        
        # Cria uma tabela padrão de 12 meses
        meses_iniciais = [f"Mês {i}" for i in range(1, 13)]
        vidas_iniciais = [1000] * 12
        valores_iniciais = [5.90] * 12
        
        df_rampa = pd.DataFrame({
            "Período": meses_iniciais,
            "Qtd. Vidas": vidas_iniciais,
            "Valor por Vida (R$)": valores_iniciais
        })
        
        # Tabela editável (estilo excel)
        dados_rampa = st.data_editor(df_rampa, num_rows="dynamic", use_container_width=True, hide_index=True)
        
        # Puxa os dados da rampa para variáveis de fallback
        qtd_vidas = dados_rampa["Qtd. Vidas"].max()
        valor_unitario = dados_rampa["Valor por Vida (R$)"].iloc[-1]
        
    else:
        col_vidas, col_preco = st.columns([1, 1])
        qtd_vidas = col_vidas.number_input("Quantidade de Vidas Fixas", min_value=1, value=1000, step=100)
        preco_calculado = calcular_preco_sugerido(qtd_vidas)
        valor_unitario = col_preco.number_input("Valor Mensal por Vida (R$)", value=float(preco_calculado), format="%.2f", step=0.10)
        
        total_mensal = qtd_vidas * valor_unitario
        st.markdown(f"""
            <div class="highlight-box">
                <h3 style="margin:0; color: #001E50;">Valor Total Mensal: R$ {total_mensal:,.2f}</h3>
                <p style="margin:0; color: #555;">Faixa aplicada: {qtd_vidas} vidas a R$ {valor_unitario:.2f} por beneficiário.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # SEÇÃO 3: ESCOPO AVANÇADO
    st.subheader("3. Configuração de Escopo e Diferenciais Estratégicos")
    
    c_scope1, c_scope2 = st.columns(2)
    
    with c_scope1:
        st.markdown("**Core Clínico (Incluso):**")
        st.checkbox("Clínico Geral 24/7", value=True, disabled=True)
        st.checkbox("Pediatria e Médico da Família", value=True)
        st.checkbox("Psicologia Orientativa (09h às 18h)", value=True)
        st.checkbox("Programa de Apoio ao Luto / Acolhimento", value=True)
        st.checkbox("App e Dashboard White Label", value=True, disabled=True)
    
    with c_scope2:
        st.markdown("**Diferenciais B2B:**")
        inc_televet = st.checkbox("Televeterinária (Pet)", value=False)
        inc_entrevista = st.checkbox("Projeto de Entrevista Qualificada", value=False)
        inc_nr1 = st.checkbox("Programa de Regulamentação NR-1", value=False)
        inc_protocolos = st.checkbox("Protocolos (Tirzepatida/Canabidiol)", value=False)
        inc_cabine = st.checkbox("Cabine Física de Telemedicina", value=False)
    
    obs_comerciais = st.text_area("Observações Comerciais (Ex: Carência, Setup de Implantação)", height=80)

    # BOTÃO GERADOR
    st.markdown("---")
    submit_btn = st.button("GERAR PROPOSTA ENTERPRISE (PDF) 🚀")

    # --- PROCESSAMENTO DO PDF ---
    if submit_btn:
        if not cliente_empresa:
            st.error("⚠️ Por favor, preencha o nome da Empresa Cliente.")
        else:
            try:
                pdf = ProposalPDF(logo_path=logo_final)
                pdf.add_page()
                
                # --- CAPA ---
                pdf.set_font('Arial', 'B', 12)
                pdf.set_text_color(*COR_PRIMARIA)
                pdf.cell(0, 10, limpa_texto(f"À/C: {cliente_empresa}"), 0, 1)
                pdf.set_font('Arial', '', 11)
                if cliente_responsavel: pdf.cell(0, 6, limpa_texto(f"Aos cuidados de: {cliente_responsavel}"), 0, 1)
                pdf.cell(0, 6, f"Data da Emissão: {datetime.now().strftime('%d/%m/%Y')}", 0, 1)
                
                pdf.ln(8)
                
                # --- INTRODUÇÃO ENTERPRISE ---
                pdf.chapter_title(f"1. A CLÍNICA DIGITAL {nome_fantasia_cliente.upper()}")
                pdf.body_text(
                    f"A LSX Medical propõe transformar sua base de confiança em um cuidado contínuo de alto valor agregado. "
                    f"Nosso objetivo é estruturar e operar uma Clínica Digital de telemedicina totalmente personalizada, "
                    f"exclusiva e integralmente sob a marca {nome_fantasia_cliente}."
                )
                pdf.body_text(
                    "Não se trata de uma plataforma genérica de mercado. Esta é uma operação desenhada para a realidade, "
                    f"estratégia de negócios e posicionamento institucional da {nome_fantasia_cliente}."
                )

                # --- JORNADA PERSONALIZADA ---
                pdf.chapter_title("2. JORNADA 100% PERSONALIZADA (WHITE LABEL)")
                pdf.bullet_point(f"Plataforma completa com identidade visual, nome e posicionamento da {nome_fantasia_cliente}.")
                pdf.bullet_point("Helpdesk e corpo clínico treinado, atuando como extensão oficial da sua equipe.")
                pdf.bullet_point(f"Atestados, receituários ICP-Brasil e exames emitidos com a marca {nome_fantasia_cliente}.")
                pdf.bullet_point("Dashboard exclusivo corporativo com dados reais de uso, engajamento e performance da base.")

                # --- ESCOPO CORE ---
                pdf.chapter_title("3. ESCOPO MÉDICO E ASSISTENCIAL")
                
                pdf.sub_title("Pronto Atendimento 24h / 7 Dias")
                pdf.body_text("Acesso imediato e ilimitado para triagem, diagnóstico e prescrição. Corpo clínico composto por:")
                pdf.bullet_point("Clínico Geral")
                pdf.bullet_point("Pediatra")
                pdf.bullet_point("Médico da Família")

                pdf.sub_title("Saúde Mental e Apoio ao Luto")
                pdf.body_text("Atendimento de Psicologia Orientativa (das 09h às 18h). Como pilar central do projeto, estruturamos o programa de Apoio ao Luto e Acolhimento Familiar.")
                pdf.body_text("Sabemos que a dor não termina no momento da despedida — muitas vezes ela se intensifica nos dias seguintes. Oferecemos escuta qualificada e direcionamento emocional para as famílias num momento extremamente sensível, fortalecendo laços e gerando valor social à marca.")

                # --- DIFERENCIAIS ESTRATÉGICOS ---
                diferenciais = []
                if inc_televet: diferenciais.append("Televeterinária (cuidado ampliado para o bem-estar de toda a família).")
                if inc_entrevista: diferenciais.append("Projeto de Entrevista Qualificada (inteligência de dados da base).")
                if inc_nr1: diferenciais.append("Programa de Regulamentação NR-1 (oportunidade de escala B2B).")
                if inc_protocolos: diferenciais.append("Protocolos clínicos estruturados para prescrição de Tirzepatida e Canabidiol.")
                if inc_cabine: diferenciais.append("Fornecimento de Cabine Física de Telemedicina para alocação presencial.")

                if diferenciais:
                    pdf.ln(3)
                    pdf.sub_title("Diferenciais Estratégicos Agregados")
                    for d in diferenciais:
                        pdf.bullet_point(d)

                # --- INVESTIMENTO E RAMPA ---
                pdf.add_page()
                pdf.chapter_title("4. MODELO DE INVESTIMENTO")
                
                if usar_rampa and dados_rampa is not None:
                    pdf.body_text("Projeção de implantação com Rampa de Lançamento (Crescimento Escalonado):")
                    pdf.ln(3)
                    
                    # Desenha Cabeçalho da Tabela
                    pdf.set_font('Arial', 'B', 10)
                    pdf.set_fill_color(*COR_PRIMARIA)
                    pdf.set_text_color(255, 255, 255)
                    pdf.cell(40, 8, 'Período', 1, 0, 'C', fill=True)
                    pdf.cell(50, 8, 'Vidas Estimadas', 1, 0, 'C', fill=True)
                    pdf.cell(50, 8, 'Valor Unitário', 1, 0, 'C', fill=True)
                    pdf.cell(50, 8, 'Faturamento Estimado', 1, 1, 'C', fill=True)

                    # Desenha as Linhas da Tabela
                    pdf.set_font('Arial', '', 10)
                    pdf.set_text_color(50, 50, 50)
                    total_ano = 0
                    
                    for index, row in dados_rampa.iterrows():
                        mes = str(row['Período'])
                        vidas = int(row['Qtd. Vidas'])
                        valor = float(row['Valor por Vida (R$)'])
                        total_mes = vidas * valor
                        total_ano += total_mes
                        
                        pdf.cell(40, 8, limpa_texto(mes), 1, 0, 'C')
                        pdf.cell(50, 8, f"{vidas:,}", 1, 0, 'C')
                        pdf.cell(50, 8, f"R$ {valor:,.2f}", 1, 0, 'C')
                        pdf.cell(50, 8, f"R$ {total_mes:,.2f}", 1, 1, 'C')
                        
                    pdf.ln(5)
                    pdf.set_font('Arial', 'B', 11)
                    pdf.set_text_color(*COR_SECUNDARIA)
                    pdf.cell(0, 8, f"Expectativa de Faturamento Acumulado no Período: R$ {total_ano:,.2f}", 0, 1, 'R')

                else:
                    # Modelo Padrão (Sem Rampa)
                    pdf.set_fill_color(*COR_CINZA_CLARO)
                    pdf.rect(10, pdf.get_y(), 190, 40, 'F')
                    pdf.set_y(pdf.get_y() + 5)
                    
                    pdf.set_font('Arial', 'B', 12)
                    pdf.set_text_color(*COR_PRIMARIA)
                    pdf.cell(95, 10, limpa_texto("QUANTIDADE DE VIDAS"), 0, 0, 'C')
                    pdf.cell(95, 10, limpa_texto("VALOR MENSAL POR VIDA"), 0, 1, 'C')
                    
                    pdf.set_font('Arial', '', 14)
                    pdf.set_text_color(50, 50, 50)
                    pdf.cell(95, 10, limpa_texto(f"{qtd_vidas} Beneficiários ativos"), 0, 0, 'C')
                    
                    pdf.set_font('Arial', 'B', 22)
                    pdf.set_text_color(*COR_SECUNDARIA) 
                    pdf.cell(95, 10, f"R$ {valor_unitario:,.2f}", 0, 1, 'C')
                    
                    pdf.ln(10)
                    pdf.set_font('Arial', 'B', 13)
                    pdf.set_text_color(*COR_PRIMARIA)
                    pdf.cell(0, 10, f"TOTAL MENSAL ESTIMADO: R$ {total_mensal:,.2f}", 0, 1, 'R')
                
                pdf.ln(8)
                pdf.sub_title("Diretrizes Comerciais:")
                pdf.bullet_point("Vigência Contratual: 24 meses (Período mínimo).")
                pdf.bullet_point("Reajuste: Anual com base no índice IPCA.")
                if obs_comerciais:
                    pdf.bullet_point(f"Observações: {obs_comerciais}")

                # --- SEGURANCA LEGAL ---
                pdf.ln(5)
                pdf.chapter_title("5. COMPROMISSO ÉTICO, SEGURANÇA E LEGALIDADE")
                texto_compliance = (
                    "O ecossistema LSX Medical é 100% seguro, auditável e estruturado para proteger sua marca e "
                    "a vida dos beneficiários, cumprindo rigorosamente as exigências legais vigentes no país:\n\n"
                    f"• REGULARIDADE TÉCNICA E ÉTICA: Operação registrada no Conselho Regional de Medicina "
                    f"do Paraná sob o nº {REGISTRO_CRM_PJ}, supervisionada diretamente por responsabilidade médica.\n\n"
                    "• PRIVACIDADE (LGPD): Total conformidade com a Lei Geral de Proteção de Dados (Lei 13.709/18). "
                    "Os prontuários médicos são criptografados e acessíveis exclusivamente na relação Médico-Paciente.\n\n"
                    "• DIRETRIZES TÉCNICAS (NR-1 e CFM): Triagem clínica rigorosa, fluxos de contingência para alto "
                    "risco e Termo de Consentimento Livre e Esclarecido (TCLE) implementado."
                )
                
                pdf.set_fill_color(250, 250, 250)
                pdf.set_draw_color(200, 200, 200)
                pdf.set_font('Arial', '', 9)
                pdf.multi_cell(0, 5, limpa_texto(texto_compliance), border=1, align='J', fill=True)

                pdf.ln(15)
                
                # --- ASSINATURA AJUSTADA PARA NÃO SOBREPOR RODAPÉ ---
                # Aumentei o espaçamento da base para garantir que o rodapé e a linha azul não sejam atropelados
                pdf.set_y(-75) 
                
                pdf.set_font('Arial', 'I', 10)
                pdf.set_text_color(100, 100, 100)
                pdf.cell(0, 5, limpa_texto("Estamos à inteira disposição para agendar uma reunião de fechamento e kick-off."), 0, 1, 'C')
                pdf.ln(5)
                
                y_ass = pdf.get_y()
                pdf.set_draw_color(*COR_PRIMARIA)
                pdf.line(70, y_ass, 140, y_ass)
                pdf.ln(3)
                
                pdf.set_font('Arial', 'B', 11)
                pdf.set_text_color(*COR_PRIMARIA)
                pdf.cell(0, 5, limpa_texto(nome_vendedor), 0, 1, 'C')
                
                pdf.set_font('Arial', '', 10)
                pdf.set_text_color(*COR_SECUNDARIA)
                pdf.cell(0, 5, limpa_texto(cargo_vendedor), 0, 1, 'C')
                
                pdf.set_font('Arial', '', 9)
                pdf.set_text_color(100, 100, 100)
                contato_str = ""
                if telefone_vendedor: contato_str += f"{telefone_vendedor} "
                if email_vendedor: contato_str += f"| {email_vendedor}"
                if contato_str:
                    pdf.cell(0, 5, limpa_texto(contato_str.strip(' |')), 0, 1, 'C')

                # Geração
                nome_arquivo = f"Proposta_LSX_{cliente_empresa.replace(' ', '_')}.pdf"
                pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace') 
                
                st.success("✅ Proposta Enterprise Gerada com Sucesso!")
                st.download_button(
                    label="⬇️ BAIXAR PROPOSTA COMERCIAL (PDF)",
                    data=pdf_bytes,
                    file_name=nome_arquivo,
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")

if __name__ == "__main__":
    main()
