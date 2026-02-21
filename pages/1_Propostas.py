import streamlit as st
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

# Limpeza de caracteres não suportados pelo FPDF padrão
def limpa_texto(texto):
    if not texto: return ""
    replacements = {"•": "-", "–": "-", "—": "-", "“": '"', "”": '"', "\u2022": "-", "\u2028": "\n"}
    for char, rep in replacements.items():
        texto = texto.replace(char, rep)
    return texto.encode('latin-1', 'replace').decode('latin-1')

# ==============================================================================
# 2. MOTOR DE PRECIFICAÇÃO DINÂMICA
# ==============================================================================
def calcular_preco_sugerido(vidas):
    """Retorna o valor por vida baseado no tier do contrato"""
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
        # Fundo Branco no cabeçalho
        self.set_fill_color(255, 255, 255)
        self.rect(0, 0, 210, 35, 'F')
        
        # Inserção da Logo
        if self.logo_path and os.path.exists(self.logo_path):
            self.image(self.logo_path, x=10, y=8, w=45) 
        else:
            self.set_font('Arial', 'B', 24)
            self.set_text_color(*COR_PRIMARIA)
            self.set_xy(10, 10)
            self.cell(0, 10, "LSX MEDICAL", 0, 0)

        # Textos do Cabeçalho
        self.set_y(10)
        self.set_font('Arial', 'B', 15)
        self.set_text_color(*COR_PRIMARIA)
        self.cell(0, 8, 'PROPOSTA COMERCIAL', 0, 1, 'R')
        
        self.set_font('Arial', 'B', 9)
        self.set_text_color(*COR_SECUNDARIA)
        self.cell(0, 5, limpa_texto('SUA MARCA, NOSSA TECNOLOGIA.'), 0, 1, 'R')
        
        # Linha decorativa Turquesa
        self.set_fill_color(*COR_SECUNDARIA)
        self.rect(10, 32, 190, 0.8, 'F')
        self.ln(12)

    def footer(self):
        # Move o cursor para 28mm antes do fim da página
        self.set_y(-28)
        
        # Desenha a linha azul turquesa PRIMEIRO
        y_line = self.get_y()
        self.set_fill_color(*COR_SECUNDARIA)
        self.rect(0, y_line, 210, 1.5, 'F')
        
        # Desce um pouquinho para não encostar na linha e escreve o texto
        self.set_y(y_line + 3)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        
        texto_rodape = f"{EMPRESA_NOME} | CNPJ: {EMPRESA_CNPJ}\n{EMPRESA_ENDERECO}\nResp. Técnico: {RESPONSAVEL_TECNICO} | {REGISTRO_CRM_PJ}"
        self.multi_cell(0, 4, limpa_texto(texto_rodape), 0, 'C')
        
        # Número da página
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

    # --- SIDEBAR: DADOS DO VENDEDOR ---
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
    st.markdown("Plataforma White Label de Saúde Integrada - Operação Comercial")

    # SEÇÃO 1: CLIENTE
    st.subheader("1. Dados do Cliente (Contratante)")
    col1, col2 = st.columns(2)
    cliente_empresa = col1.text_input("Razão Social / Empresa", placeholder="Ex: Grupo Alfa")
    cliente_responsavel = col2.text_input("Nome do Responsável", placeholder="Ex: João Silva")
    
    st.markdown("---")
    
    # SEÇÃO 2: PRECIFICAÇÃO REATIVA
    st.subheader("2. Dimensionamento e Precificação")
    
    col_vidas, col_preco = st.columns([1, 1])
    qtd_vidas = col_vidas.number_input("Quantidade de Vidas (Beneficiários)", min_value=1, value=100, step=10)
    
    preco_calculado = calcular_preco_sugerido(qtd_vidas)
    
    valor_unitario = col_preco.number_input(
        "Valor Mensal por Vida (R$)", 
        value=float(preco_calculado), 
        format="%.2f",
        step=0.10
    )
    
    total_mensal = qtd_vidas * valor_unitario
    
    st.markdown(f"""
        <div class="highlight-box">
            <h3 style="margin:0; color: #001E50;">Valor Total Mensal: R$ {total_mensal:,.2f}</h3>
            <p style="margin:0; color: #555;">Faixa aplicada: {qtd_vidas} vidas a R$ {valor_unitario:.2f} por beneficiário.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # SEÇÃO 3: ESCOPO
    st.subheader("3. Configuração da Solução (Escopo)")
    c_scope1, c_scope2 = st.columns(2)
    
    with c_scope1:
        st.markdown("**Incluso no Pacote (Padrão):**")
        st.checkbox("Pronto Atendimento Digital 24h", value=True, disabled=True)
        st.checkbox("Receita, Atestados e Pedidos de Exames", value=True, disabled=True)
        st.checkbox("Plataforma White Label (Personalização Visual)", value=True, disabled=True)
        st.checkbox("Clube de Vantagens (Até 60% de desconto)", value=True, disabled=True)
    
    with c_scope2:
        st.markdown("**Adicionais / Opcionais:**")
        incluir_psico = st.checkbox("Incluir Psicologia (Plantão de Acolhimento)", value=False)
        incluir_nutri = st.checkbox("Incluir Nutrição (Orientação)", value=False)
        modelo_especialistas = st.selectbox("Especialistas (Mais de 30 áreas)", 
            ["Pay-per-use (Usuário paga coparticipação)", "Incluso (Empresa paga)", "Não incluso"])
    
    obs_comerciais = st.text_area("Observações Comerciais (Ex: Carência, Implantação guiada)", height=80)

    # BOTÃO GERADOR
    st.markdown("---")
    submit_btn = st.button("GERAR PROPOSTA LSX (PDF) 🚀")

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
                
                # --- INTRODUÇÃO ---
                pdf.chapter_title("1. LANCE SUA CLÍNICA DIGITAL COM A LSX")
                pdf.body_text(
                    "A LSX MEDICAL entrega para sua operação total tranquilidade. Uma plataforma white-label "
                    "robusta para clínicas, redes, operadoras e empreendedores que desejam iniciar sua operação "
                    "de forma ágil, contando com atendimento médico de excelência 24 horas por dia, 7 dias por semana."
                )

                # --- DIFERENCIAIS ---
                pdf.chapter_title("2. O QUE NOSSA PLATAFORMA OFERECE")
                pdf.body_text("Veja como sua operação nasce pronta e estruturada com nossos grandes diferenciais:")
                
                pdf.bullet_point("Personalização Visual: Um painel intuitivo para começar a atender com a sua marca e regras de negócio.")
                pdf.bullet_point("Onboarding Guiado: Implementação rápida com equipe médica já 100% integrada ao sistema.")
                pdf.bullet_point("Agendamento Facilitado: Plataforma simples e de fácil acesso, colocando a saúde na palma da mão do seu usuário.")
                pdf.bullet_point("Clube de Desconto: Benefícios exclusivos para clientes com até 60% de desconto.")
                pdf.bullet_point("Solicitação de Exames e Receitas: Médicos emitem documentação com assinatura digital ICP-Brasil diretamente pelo aplicativo.")

                # --- ESCOPO ---
                pdf.chapter_title("3. ESCOPO DOS SERVIÇOS")
                
                pdf.sub_title("Pronto Atendimento (Telemedicina Clínico e Familiar)")
                pdf.body_text("Consulte um médico em qualquer hora e lugar. Independente do horário, sempre haverá um especialista qualificado à sua disposição para o cuidado primário e direcionamento clínico.")
                
                if incluir_psico:
                    pdf.sub_title("Saúde Mental (Telepsicologia)")
                    pdf.body_text("Serviço de acolhimento psicológico focado no bem-estar emocional, oferecendo escuta qualificada e acompanhamento breve e resolutivo.")

                if incluir_nutri:
                    pdf.sub_title("Orientação Nutricional")
                    pdf.body_text("Acompanhamento focado em reeducação alimentar e bem-estar físico preventivo.")

                pdf.sub_title("Consultas com Especialistas")
                if modelo_especialistas == "Pay-per-use (Usuário paga coparticipação)":
                    pdf.body_text("Acesso a um corpo clínico com mais de 30 especialidades prontas para atender, mediante agendamento e pagamento de coparticipação pelo usuário com valores reduzidos.")
                elif modelo_especialistas == "Incluso (Empresa paga)":
                    pdf.body_text("Pacote de consultas eletivas em diversas especialidades médicas, previamente cobertas pela contratante e geridas através de nosso painel corporativo.")

                # --- INVESTIMENTO ---
                pdf.add_page()
                pdf.chapter_title("4. INVESTIMENTO E CONDIÇÕES COMERCIAIS")
                
                pdf.set_fill_color(*COR_CINZA_CLARO)
                pdf.rect(10, pdf.get_y(), 190, 40, 'F')
                pdf.set_y(pdf.get_y() + 5)
                
                pdf.set_font('Arial', 'B', 12)
                pdf.set_text_color(*COR_PRIMARIA)
                pdf.cell(95, 10, limpa_texto("QUANTIDADE DE VIDAS"), 0, 0, 'C')
                pdf.cell(95, 10, limpa_texto("VALOR MENSAL POR VIDA"), 0, 1, 'C')
                
                pdf.set_font('Arial', '', 14)
                pdf.set_text_color(50, 50, 50)
                pdf.cell(95, 10, limpa_texto(f"{qtd_vidas} Beneficiários"), 0, 0, 'C')
                
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
                pdf.bullet_point("Reajuste: Anual com base no IPCA.")
                pdf.bullet_point("Suporte: Gerente de Contas dedicado e Help Desk 100% especializado.")
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

                # --- ASSINATURA DINAMICA ---
                # Ajuste: Sobe a assinatura para Y = -62 para não sobrepor o rodapé
                pdf.set_y(-62)
                
                pdf.set_font('Arial', 'I', 10)
                pdf.set_text_color(100, 100, 100)
                pdf.cell(0, 5, limpa_texto("Estamos à inteira disposição para agendar uma reunião de fechamento e kick-off."), 0, 1, 'C')
                
                # Ajuste: Espaçamento menor (5) antes da linha
                pdf.ln(5)
                
                y_ass = pdf.get_y()
                pdf.set_draw_color(*COR_PRIMARIA)
                pdf.line(70, y_ass, 140, y_ass)
                
                # Ajuste: Espaçamento menor (2) depois da linha
                pdf.ln(2)
                
                # Puxa os dados da barra lateral
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

                # Geração do Arquivo
                nome_arquivo = f"Proposta_LSX_{cliente_empresa.replace(' ', '_')}.pdf"
                pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace') 
                
                st.success("✅ Proposta Gerada e Validada!")
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
