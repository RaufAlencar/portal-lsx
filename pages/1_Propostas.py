import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os

# ==============================================================================
# 1. IDENTIDADE VISUAL & DADOS CORPORATIVOS
# ==============================================================================
COR_PRIMARIA = (0, 30, 80)      
COR_SECUNDARIA = (0, 195, 180)  
COR_CINZA_CLARO = (245, 246, 250)

EMPRESA_NOME = "LSX MEDICAL LTDA"
EMPRESA_CNPJ = "53.210.447/0001-51"
EMPRESA_ENDERECO = "Alameda Dr. Carlos de Carvalho, 431 - 12º Andar | Curitiba - PR"
EMPRESA_SITE = "www.lsxmedical.com.br"
RESPONSAVEL_TECNICO = "Dra. Michelle Massaki | CRM-PR 28.435"
REGISTRO_CRM_PJ = "CRM-PR PJ 24.806"

# ==============================================================================
# 1.5. MOTOR DE INTELIGÊNCIA COMERCIAL (SEGMENTOS B2B)
# ==============================================================================
TEXTOS_SEGMENTOS = {
    "Cartões de Benefícios / Saúde": {
        "intro1": "Para aumentar o LTV (Life Time Value) e a atratividade do seu cartão, a LSX Medical oferece a infraestrutura completa para você operar a sua própria Clínica Digital de Telemedicina, fortalecendo o ecossistema da {marca}.",
        "intro2": "Entregue um benefício de uso imediato e alta percepção de valor. Uma solução 100% customizável, pronta para escalar suas vendas e gerar novas linhas de receita, sem a necessidade de investir em desenvolvimento tecnológico ou corpo clínico próprio.",
        "titulo_mental": "Telepsicologia Orientativa (Acesso Rápido)",
        "texto_mental": "Atendimento das 09h às 18h. Agregue alto valor percebido ao seu cartão entregando cuidado emocional.\n\nNossos profissionais estão disponíveis para triagem e orientação em casos de ansiedade, crises pontuais e conflitos familiares. Um benefício que gera uso recorrente e fideliza o usuário ao seu produto."
    },
    "Geral / Corporativo": {
        "intro1": "A LSX Medical propõe transformar sua base de confiança em um cuidado contínuo de alto valor agregado. Nosso objetivo é estruturar e operar uma Clínica Digital de telemedicina totalmente personalizada, exclusiva e integralmente sob a marca {marca}.",
        "intro2": "Não se trata de uma plataforma genérica de mercado. Esta é uma operação desenhada para a realidade corporativa, focada em reduzir absenteísmo, otimizar custos de saúde e valorizar a sua marca empregadora perante colaboradores e clientes.",
        "titulo_mental": "Telepsicologia Orientativa (Suporte Corporativo)",
        "texto_mental": "Atendimento das 09h às 18h. Entendemos que a saúde mental é o maior desafio corporativo atual.\n\nDisponibilizamos suporte psicológico de rápido acesso para gerenciamento de estresse, ansiedade e prevenção de burnout, promovendo bem-estar e produtividade para os seus beneficiários."
    },
    "Funerárias / Assistência Familiar": {
        "intro1": "No setor de assistência familiar, o cuidado não termina com a despedida. A LSX Medical propõe transformar a {marca} em uma verdadeira provedora de saúde em vida, agregando valor tangível aos seus planos e aumentando a fidelização e retenção da sua carteira.",
        "intro2": "Desenhamos uma Clínica Digital 100% White Label. O grande diferencial desta proposta é o foco em Saúde Mental e Apoio ao Luto, oferecendo suporte contínuo para a família no momento em que ela mais precisa, consolidando a sua marca como um pilar de acolhimento.",
        "titulo_mental": "Telepsicologia Orientativa (Apoio ao Luto)",
        "texto_mental": "Atendimento das 09h às 18h. Como pilar central do projeto, estruturamos o programa de Apoio ao Luto e Acolhimento Familiar.\n\nSabemos que a dor não termina no momento da despedida — muitas vezes ela se intensifica nos dias seguintes. Oferecemos escuta qualificada e direcionamento emocional num momento extremamente sensível, fortalecendo laços e gerando valor social à marca."
    },
    "Hospitais, Clínicas e Planos de Saúde": {
        "intro1": "A LSX Medical atua como o braço tecnológico e de retaguarda médica da {marca}. Nossa solução de Clínica Digital visa otimizar sua operação, desafogar prontos-socorros físicos e expandir sua capilaridade de atendimento.",
        "intro2": "Com protocolos integrados e fluxos de triagem digital (Pronto Atendimento Virtual), reduzimos custos operacionais e sinistralidade, garantindo a excelência do cuidado primário e o direcionamento inteligente de casos de alta complexidade para a sua rede física.",
        "titulo_mental": "Telepsicologia Orientativa (Triagem)",
        "texto_mental": "Atendimento das 09h às 18h. Atua como um importante filtro para a rede presencial.\n\nRealizamos o acolhimento, escuta qualificada e encaminhamento assertivo. Ideal para pacientes com quadros leves, evitando idas desnecessárias à emergência e oferecendo conforto e comodidade diretamente pelo aplicativo."
    },
    "Varejo e Grandes Redes": {
        "intro1": "O varejo moderno exige inovação na retenção de clientes e na monetização da base. A LSX propõe que a {marca} ofereça saúde de qualidade como um serviço financeiro e de fidelidade (Health as a Service).",
        "intro2": "Com nossa plataforma White Label, você entrega um benefício percebido como essencial, aumentando o engajamento do cliente com o seu ecossistema, gerando recorrência e abrindo uma nova frente de faturamento altamente rentável.",
        "titulo_mental": "Telepsicologia Orientativa (Bem-Estar)",
        "texto_mental": "Atendimento das 09h às 18h. Diferencie o seu programa de fidelidade entregando acolhimento.\n\nOferecemos acesso rápido a profissionais de saúde mental para orientações gerais. Um serviço moderno que conecta a sua marca diretamente ao cuidado pessoal do seu cliente."
    }
}


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

# FUNÇÃO DE LIMPEZA BLINDADA
def limpa_texto(texto):
    if not texto: return ""
    texto = str(texto)
    replacements = {
        "•": "-", "–": "-", "—": "-", "“": '"', "”": '"', "‘": "'", "’": "'", 
        "\u2022": "-", "\u2028": "\n"
    }
    for char, rep in replacements.items():
        texto = texto.replace(char, rep)
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
        self.set_auto_page_break(auto=True, margin=30) 

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
        self.cell(0, 8, 'PROPOSTA COMERCIAL / ANEXO I', 0, 1, 'R')
        
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
        if self.get_y() > 240: 
            self.add_page()
        self.ln(5)
        self.set_font('Arial', 'B', 11)
        self.set_text_color(*COR_PRIMARIA)
        self.cell(0, 8, limpa_texto(title.upper()), 0, 1, 'L')
        self.set_fill_color(*COR_PRIMARIA)
        self.rect(10, self.get_y(), 10, 0.8, 'F')
        self.ln(3)

    def sub_title(self, title):
        if self.get_y() > 250: 
            self.add_page()
        self.set_font('Arial', 'B', 10)
        self.set_text_color(*COR_PRIMARIA)
        self.cell(0, 6, limpa_texto(title), 0, 1, 'L')
        self.ln(1)

    def body_text(self, text):
        self.set_font('Arial', '', 9)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5, limpa_texto(text), align='J')
        self.ln(2)

    def bullet_point(self, text):
        self.set_font('Arial', '', 9)
        self.set_text_color(50, 50, 50)
        self.cell(5) 
        self.set_text_color(*COR_SECUNDARIA)
        self.cell(3, 5, chr(187), 0, 0) 
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
        email_vendedor = st.text_input("E-mail", value="")
        
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
    st.title("Gerador de Propostas e Anexo I - LSX Medical")
    st.markdown("Plataforma White Label B2B - Configuração de Contratos Avançados")

    st.subheader("1. Dados do Cliente e Inteligência Comercial")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    cliente_empresa = col1.text_input("Razão Social / Empresa", value="")
    cliente_responsavel = col2.text_input("Nome do Responsável", value="")
    segmento_selecionado = col3.selectbox("Segmento de Atuação", list(TEXTOS_SEGMENTOS.keys()))
    
    nome_fantasia_cliente = cliente_empresa if cliente_empresa else "Sua Empresa"

    st.markdown("---")
    
    st.subheader("2. Dimensionamento, Precificação e Prazos")
    col_vig, col_acesso, col_pag = st.columns([1, 1, 1])
    vigencia_contrato = col_vig.radio("Vigência do Contrato", ["12 Meses", "24 Meses"], index=1)
    
    data_acesso = col_acesso.text_input("Data Disponibilização do Acesso", value="")
    data_pagamento = col_pag.text_input("Data 1º Pagamento / Kick-Off", value="")
    
    st.markdown("<br>", unsafe_allow_html=True)
    usar_rampa = st.checkbox("📈 Habilitar Cronograma de Implantação (Rampa de Crescimento)")
    dados_rampa = None 
    
    qtd_vidas = 1000 
    
    if usar_rampa:
        st.info("Preencha a rampa. A política de escalonamento será gerada baseada nessas linhas.")
        
        meses_iniciais = ["Mês 1", "Mês 2", "Mês 3", "Mês 4"] 
        vidas_iniciais = [1000, 3000, 5000, 10000]
        valores_iniciais = [3.90, 3.90, 3.90, 3.90]
        
        df_rampa = pd.DataFrame({
            "Período": meses_iniciais, "Vidas Contratadas": vidas_iniciais, "Valor por Vida (R$)": valores_iniciais
        })
        dados_rampa = st.data_editor(df_rampa, num_rows="dynamic", use_container_width=True, hide_index=True)
        dados_rampa = dados_rampa.fillna(0)
        
        try:
            qtd_vidas = int(dados_rampa["Vidas Contratadas"].max())
            valor_unitario = float(dados_rampa["Valor por Vida (R$)"].iloc[-1])
        except:
            qtd_vidas = 10000
            valor_unitario = 3.90
    else:
        col_vidas, col_preco = st.columns([1, 1])
        qtd_vidas = col_vidas.number_input("Volume Inicial Estimado (Vidas)", min_value=1, value=1000, step=100)
        if qtd_vidas is None: qtd_vidas = 0 
        
        preco_calculado = calcular_preco_sugerido(qtd_vidas)
        valor_unitario = col_preco.number_input("Valor Mensal por Vida (R$)", value=float(preco_calculado), format="%.2f", step=0.10)
        if valor_unitario is None: valor_unitario = 0.0 
        
        total_mensal = qtd_vidas * valor_unitario
        st.markdown(f"""
            <div class="highlight-box">
                <h3 style="margin:0; color: #001E50;">Investimento Base: R$ {total_mensal:,.2f} /mês</h3>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("3. Escopo Bônus e Serviços Adicionais (Precificação)")
    st.write("Marque os diferenciais contratados. Se houver custo extra, o sistema abrirá os campos para precificação automática no contrato.")
    
    inc_clube = st.checkbox("Clube de Benefícios (Gratuito Inclusivo)", value=True)
    
    inc_televet = st.checkbox("Televeterinária (Pet)")
    if inc_televet:
        col_t1, col_t2 = st.columns(2)
        qtd_pet = col_t1.number_input("Quantidade de Vidas Pet", min_value=1, value=1000)
        valor_pet = col_t2.number_input("Valor por Vida Pet (R$)", min_value=0.0, value=1.00, format="%.2f")

    inc_entrevista = st.checkbox("Projeto de Entrevista Qualificada")
    if inc_entrevista:
        col_e1, col_e2, col_e3 = st.columns(3)
        plano_entrevista = col_e1.text_input("Formato (Entrevista)", value="Fixo Mensal")
        valor_entrevista = col_e2.number_input("Valor Unitário/Mensal (R$) - Entrevista", min_value=0.0, value=1500.00, format="%.2f")
        setup_entrevista = col_e3.number_input("Setup (R$) - Entrevista", min_value=0.0, value=0.00, format="%.2f")

    inc_nr1 = st.checkbox("Programa de Regulamentação NR-1")
    if inc_nr1:
        col_n1, col_n2, col_n3 = st.columns(3)
        plano_nr1 = col_n1.text_input("Formato (NR-1)", value="Por Vidas Contratadas")
        valor_nr1 = col_n2.number_input("Valor Unitário/Mensal (R$) - NR-1", min_value=0.0, value=1.50, format="%.2f")
        setup_nr1 = col_n3.number_input("Setup (R$) - NR-1", min_value=0.0, value=0.00, format="%.2f")

    inc_protocolos = st.checkbox("Protocolos Clínicos Personalizados")
    if inc_protocolos:
        col_p1, col_p2, col_p3 = st.columns(3)
        plano_protocolos = col_p1.text_input("Formato (Protocolos)", value="Taxa Única de Estruturação")
        valor_protocolos = col_p2.number_input("Mensalidade (R$) - Protocolos", min_value=0.0, value=0.00, format="%.2f")
        setup_protocolos = col_p3.number_input("Setup/Taxa Única (R$) - Protocolos", min_value=0.0, value=3000.00, format="%.2f")

    inc_cabine = st.checkbox("Cabine Física de Telemedicina")
    if inc_cabine:
        col_c1, col_c2 = st.columns(2)
        qtd_cabines = col_c1.number_input("Quantidade de Cabines", min_value=1, value=1)
        default_cabine = 0.00 if qtd_vidas >= 100000 else 3900.00
        valor_cabine = col_c2.number_input("Mensalidade por Cabine (R$)", min_value=0.0, value=default_cabine, format="%.2f")
        
        if valor_cabine == 0:
            st.success(f"🎉 Como o contrato atinge {qtd_vidas:,} vidas, a cabine será fornecida em regime de Comodato (Gratuita)!")
        else:
            st.info("ℹ️ Instalação Gratuita. O contrato da cabine acompanhará a vigência principal.")

    st.markdown("---")
    obs_comerciais = st.text_area("Observações Comerciais (Ex: Carência, Alinhamentos Específicos)", height=80)

    submit_btn = st.button("GERAR ANEXO COMERCIAL (PDF) 🚀")

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
                if data_acesso: pdf.cell(0, 6, f"Data da Emissão: {datetime.now().strftime('%d/%m/%Y')}", 0, 1)
                pdf.ln(5)
                
                # --- APRESENTAÇÃO COMERCIAL ---
                copy_intro = TEXTOS_SEGMENTOS[segmento_selecionado]
                pdf.chapter_title(f"A CLÍNICA DIGITAL {nome_fantasia_cliente.upper()}")
                pdf.body_text(copy_intro["intro1"].replace("{marca}", nome_fantasia_cliente))
                pdf.body_text(copy_intro["intro2"])
                pdf.ln(5)

                # ==========================================
                # ESTRUTURA RIGOROSA DO ANEXO I
                # ==========================================
                pdf.set_font('Arial', 'B', 14)
                pdf.set_text_color(*COR_PRIMARIA)
                pdf.cell(0, 8, limpa_texto("ANEXO I - CONDIÇÕES COMERCIAIS"), 0, 1, 'C')
                pdf.ln(3)

                # 1. OBJETO DO ANEXO
                pdf.chapter_title("1. OBJETO DO ANEXO")
                pdf.body_text("O presente Anexo tem por objeto estabelecer todas as condições comerciais, operacionais e assistenciais referentes à contratação da Solução de Telemedicina Corporativa em modelo White Label, conforme proposta comercial aceita pelas partes.")

                # 2. MODELO DA SOLUÇÃO CONTRATADA
                pdf.chapter_title("2. MODELO DA SOLUÇÃO CONTRATADA")
                pdf.body_text("A solução contratada compreende:")
                pdf.bullet_point("Plataforma de telemedicina 100% White Label;")
                pdf.bullet_point("Operação assistencial em regime de Pronto Atendimento 24x7;")
                pdf.bullet_point(f"Clínica digital personalizada com identidade visual da CONTRATANTE ({nome_fantasia_cliente});")
                pdf.bullet_point("Corpo clínico próprio da LSX Medical;")
                pdf.bullet_point("Operação, suporte técnico e helpdesk sob gestão da LSX Medical.")

                # 3. ESCOPO DOS SERVIÇOS INCLUSOS
                pdf.chapter_title("3. ESCOPO DOS SERVIÇOS INCLUSOS")
                pdf.body_text("Estão inclusos na solução contratada:")
                pdf.bullet_point("Agendamento digital de consultas (opcional);")
                pdf.bullet_point("Videoconsultas integradas;")
                pdf.bullet_point("Prontuário eletrônico;")
                pdf.bullet_point("Receituário médico digital;")
                pdf.bullet_point("Emissão de atestados médicos;")
                pdf.bullet_point("Solicitação de exames;")
                pdf.bullet_point("Dashboard gerencial;")
                pdf.bullet_point("Helpdesk técnico e assistencial;")
                
                if inc_clube: pdf.bullet_point("Clube de Benefícios;")
                if inc_televet: pdf.bullet_point(f"Televeterinária (Pet) estruturada para {qtd_pet:,} pets;")
                if inc_entrevista: pdf.bullet_point("Projeto de Entrevista Qualificada;")
                if inc_nr1: pdf.bullet_point("Programa de Regulamentação NR-1;")
                if inc_protocolos: pdf.bullet_point("Protocolos Clínicos Personalizados;")
                if inc_cabine: pdf.bullet_point(f"Fornecimento de {qtd_cabines} Cabine(s) Física(s) de Telemedicina;")

                # 4. MODELO ASSISTENCIAL
                pdf.chapter_title("4. MODELO ASSISTENCIAL")
                
                pdf.sub_title("4.1 Pronto Atendimento 24x7")
                pdf.body_text("Atendimento médico disponível 24 horas por dia, 7 dias por semana, com foco em orientação clínica, resolutividade e redução de atendimentos presenciais desnecessários.")
                
                pdf.sub_title("4.2 Especialidades Disponíveis")
                pdf.bullet_point("Clínico Geral;")
                pdf.bullet_point("Pediatria;")
                pdf.bullet_point("Medicina da Família;")
                
                pdf.ln(1)
                pdf.bullet_point(f"{copy_intro['titulo_mental']}:")
                for paragrafo in copy_intro["texto_mental"].split("\n\n"):
                    pdf.set_font('Arial', '', 9)
                    pdf.set_text_color(50, 50, 50)
                    pdf.cell(10) 
                    pdf.multi_cell(0, 5, limpa_texto(paragrafo), align='J')

                # 5. POLÍTICA DE ESPECIALIDADES
                pdf.chapter_title("5. POLÍTICA DE ESPECIALIDADES")
                pdf.bullet_point("Quando houver encaminhamento médico realizado pelo corpo clínico da LSX Medical e o atendimento ocorrer dentro da rede própria da LSX Medical, não haverá custo adicional;")
                pdf.bullet_point("Caso o beneficiário solicite diretamente atendimento especializado sem encaminhamento médico, poderão ser aplicadas as regras comerciais vigentes para especialidades avulsas, conforme tabela da LSX Medical.")

                # 6. CONDIÇÕES COMERCIAIS E ESCALONAMENTO DE PREÇOS
                pdf.chapter_title("6. CONDIÇÕES COMERCIAIS E ESCALONAMENTO DE PREÇOS")
                pdf.body_text("O modelo de precificação será mensal, baseado na quantidade de vidas contratada multiplicada pelo valor unitário estipulado, respeitando a estruturação abaixo:")
                
                if usar_rampa and dados_rampa is not None:
                    pdf.ln(2)
                    pdf.set_font('Arial', 'B', 9)
                    pdf.set_fill_color(*COR_PRIMARIA)
                    pdf.set_text_color(255, 255, 255)
                    pdf.cell(45, 8, 'Fase / Período', 1, 0, 'C', fill=True)
                    pdf.cell(45, 8, 'Vidas Contratadas', 1, 0, 'C', fill=True)
                    pdf.cell(45, 8, 'Valor Unitário', 1, 0, 'C', fill=True)
                    pdf.cell(45, 8, 'Investimento Mensal', 1, 1, 'C', fill=True)

                    pdf.set_font('Arial', '', 9)
                    pdf.set_text_color(50, 50, 50)
                    
                    for index, row in dados_rampa.iterrows():
                        mes = str(row['Período'])
                        try:
                            vidas = int(row['Vidas Contratadas'])
                            valor = float(row['Valor por Vida (R$)'])
                        except:
                            vidas, valor = 0, 0.0
                            
                        faturamento_mes = vidas * valor
                        pdf.cell(45, 6, limpa_texto(mes), 1, 0, 'C')
                        pdf.cell(45, 6, f"{vidas:,}", 1, 0, 'C')
                        pdf.cell(45, 6, f"R$ {valor:,.2f}", 1, 0, 'C')
                        pdf.cell(45, 6, f"R$ {faturamento_mes:,.2f}", 1, 1, 'C')
                
                pdf.ln(5)
                pdf.body_text("A partir de 10.001 vidas, seguindo o escalonamento abaixo para crescimento orgânico da base:")
                
                pdf.set_font('Arial', 'B', 9)
                pdf.set_fill_color(240, 240, 240)
                pdf.set_text_color(*COR_PRIMARIA)
                pdf.cell(90, 6, 'Quantidade Mínima de Vidas', 1, 0, 'C', fill=True)
                pdf.cell(90, 6, 'Valor por Vida', 1, 1, 'C', fill=True)
                
                faixas_upsell = [
                    ("10.001 a 17.999", "R$ 3,49"),
                    ("18.000 a 20.999", "R$ 2,90"),
                    ("21.000 a 23.999", "R$ 2,49"),
                    ("24.000 a 26.999", "R$ 1,90"),
                    ("27.000 a 29.999", "R$ 1,49"),
                    ("Acima de 30.000", "R$ 0,90")
                ]
                
                pdf.set_font('Arial', '', 9)
                pdf.set_text_color(50, 50, 50)
                for faixa, valor in faixas_upsell:
                    pdf.cell(90, 6, limpa_texto(faixa), 1, 0, 'C')
                    pdf.cell(90, 6, limpa_texto(valor), 1, 1, 'C')

                pdf.ln(3)
                pdf.body_text("O escalonamento ocorrerá de forma automática conforme o crescimento do número de vidas, sem necessidade de renegociação contratual, desde que respeitados os volumes mínimos estabelecidos neste acordo.")

                # ==========================================
                # SERVIÇOS ADICIONAIS (INTELIGÊNCIA DE PREÇOS)
                # ==========================================
                if inc_clube or inc_televet or inc_entrevista or inc_nr1 or inc_protocolos or inc_cabine:
                    pdf.ln(3)
                    pdf.sub_title("6.1 Condições e Precificação - Serviços Adicionais Contratados")
                    
                    if inc_clube:
                        pdf.bullet_point("Clube de Benefícios: Fornecido de forma integralmente Gratuita (Isento) para a base ativa.")
                    
                    if inc_televet:
                        pdf.bullet_point(f"Televeterinária (Pet): Pacote para {qtd_pet:,} vidas Pet ao valor de R$ {valor_pet:,.2f} por vida. Investimento de R$ {qtd_pet * valor_pet:,.2f} /mês adicionais ao plano principal.")
                        
                    if inc_entrevista:
                        txt_entrevista = f"Projeto de Entrevista Qualificada: Formato {plano_entrevista} | Valor Acordado: R$ {valor_entrevista:,.2f}"
                        if setup_entrevista > 0: txt_entrevista += f" | Setup Inicial: R$ {setup_entrevista:,.2f}"
                        pdf.bullet_point(txt_entrevista + ".")
                        
                    if inc_nr1:
                        txt_nr1 = f"Programa de Regulamentação NR-1: Formato {plano_nr1} | Valor Acordado: R$ {valor_nr1:,.2f}"
                        if setup_nr1 > 0: txt_nr1 += f" | Setup Inicial: R$ {setup_nr1:,.2f}"
                        pdf.bullet_point(txt_nr1 + ".")
                        
                    if inc_protocolos:
                        txt_prot = f"Protocolos Clínicos: Formato {plano_protocolos} | Mensalidade: R$ {valor_protocolos:,.2f}"
                        if setup_protocolos > 0: txt_prot += f" | Taxa Única de Estruturação: R$ {setup_protocolos:,.2f}"
                        pdf.bullet_point(txt_prot + ".")
                        
                    if inc_cabine:
                        if valor_cabine == 0:
                            pdf.bullet_point(f"Cabine Física de Telemedicina: {qtd_cabines} unidade(s) alocada(s) em regime de COMODATO (R$ 0,00) devido ao volume de base contratada. Instalação Gratuita. A manutenção das cabines acompanha a vigência principal.")
                        else:
                            pdf.bullet_point(f"Cabine Física de Telemedicina: {qtd_cabines} unidade(s) contratada(s) sob locação ao valor de R$ {valor_cabine:,.2f} /mês cada. Instalação Gratuita. O contrato acompanha a vigência principal.")

                    # NOVA SEÇÃO 6.2 (RESUMO DO INVESTIMENTO)
                    pdf.ln(5)
                    pdf.sub_title("6.2 Resumo do Investimento Mensal (Plataforma + Adicionais)")
                    
                    # Puxa o valor da primeira fase ou valor fixo
                    if usar_rampa and dados_rampa is not None and not dados_rampa.empty:
                        try:
                            v_ini = int(dados_rampa.iloc[0]['Vidas Contratadas'])
                            p_ini = float(dados_rampa.iloc[0]['Valor por Vida (R$)'])
                            base_faturamento = v_ini * p_ini
                            lbl_base = f"Licenciamento Plataforma (Base da 1ª Fase - {v_ini:,} vidas)"
                        except:
                            base_faturamento = qtd_vidas * valor_unitario
                            lbl_base = f"Licenciamento Plataforma ({qtd_vidas:,} vidas)"
                    else:
                        base_faturamento = qtd_vidas * valor_unitario
                        lbl_base = f"Licenciamento Plataforma ({qtd_vidas:,} vidas)"
                        
                    total_adicionais = 0
                    total_setup = 0
                    
                    pdf.set_font('Arial', '', 9)
                    pdf.set_text_color(50, 50, 50)
                    
                    pdf.cell(5)
                    pdf.cell(140, 5, limpa_texto(f"» {lbl_base}:"), 0, 0)
                    pdf.cell(0, 5, f"R$ {base_faturamento:,.2f}", 0, 1, 'R')
                    
                    if inc_televet:
                        val_t = qtd_pet * valor_pet
                        total_adicionais += val_t
                        pdf.cell(5); pdf.cell(140, 5, limpa_texto(f"» Televeterinária ({qtd_pet:,} pets):"), 0, 0); pdf.cell(0, 5, f"R$ {val_t:,.2f}", 0, 1, 'R')
                        
                    if inc_entrevista:
                        val_e = (qtd_vidas * valor_entrevista) if "vida" in plano_entrevista.lower() else valor_entrevista
                        total_adicionais += val_e
                        total_setup += setup_entrevista
                        pdf.cell(5); pdf.cell(140, 5, limpa_texto(f"» Entrevista Qualificada ({plano_entrevista}):"), 0, 0); pdf.cell(0, 5, f"R$ {val_e:,.2f}", 0, 1, 'R')
                        
                    if inc_nr1:
                        val_n = (qtd_vidas * valor_nr1) if "vida" in plano_nr1.lower() else valor_nr1
                        total_adicionais += val_n
                        total_setup += setup_nr1
                        pdf.cell(5); pdf.cell(140, 5, limpa_texto(f"» Programa NR-1 ({plano_nr1}):"), 0, 0); pdf.cell(0, 5, f"R$ {val_n:,.2f}", 0, 1, 'R')

                    if inc_protocolos and valor_protocolos > 0:
                        total_adicionais += valor_protocolos
                        pdf.cell(5); pdf.cell(140, 5, limpa_texto("» Protocolos Clínicos (Mensalidade):"), 0, 0); pdf.cell(0, 5, f"R$ {valor_protocolos:,.2f}", 0, 1, 'R')
                    if inc_protocolos:
                        total_setup += setup_protocolos

                    if inc_cabine and valor_cabine > 0:
                        val_c = qtd_cabines * valor_cabine
                        total_adicionais += val_c
                        pdf.cell(5); pdf.cell(140, 5, limpa_texto(f"» Cabine Física ({qtd_cabines} un):"), 0, 0); pdf.cell(0, 5, f"R$ {val_c:,.2f}", 0, 1, 'R')

                    pdf.ln(2)
                    pdf.set_font('Arial', 'B', 10)
                    pdf.set_text_color(*COR_PRIMARIA)
                    pdf.cell(5)
                    pdf.cell(140, 6, "INVESTIMENTO MENSAL TOTAL:", 0, 0)
                    pdf.cell(0, 6, f"R$ {(base_faturamento + total_adicionais):,.2f}", 0, 1, 'R')
                    
                    if total_setup > 0:
                        pdf.set_font('Arial', 'I', 8)
                        pdf.set_text_color(100, 100, 100)
                        pdf.cell(5)
                        pdf.cell(140, 5, "* Taxa Única de Setup/Estruturação (Adicionais) faturada na implantação:", 0, 0)
                        pdf.cell(0, 5, f"R$ {total_setup:,.2f}", 0, 1, 'R')


                # 7. MODELO DE COBRANÇA
                pdf.chapter_title("7. MODELO DE COBRANÇA")
                pdf.bullet_point("Periodicidade: mensal;")
                pdf.bullet_point("Base de cálculo: volume mínimo estipulado multiplicado pelo valor unitário por vida;")
                pdf.bullet_point("Forma de pagamento: conforme definido no contrato principal;")
                pdf.bullet_point("Não haverá cobrança de taxa de setup, implantação ou adesão da plataforma principal;")
                pdf.bullet_point("A apuração será realizada do primeiro ao último dia de cada mês;")
                pdf.bullet_point("Os pagamentos serão realizados até o dia 10 do mês subsequente.")

                # 8. IMPLANTAÇÃO E PRAZOS
                pdf.chapter_title("8. IMPLANTAÇÃO E PRAZOS")
                pdf.bullet_point("Prazo de implantação da clínica digital White Label: até 48 horas;")
                pdf.bullet_point("Prazo de implantação e configuração do Clube de Benefícios: até 20 dias;")
                pdf.bullet_point("Personalização visual conforme identidade da CONTRATANTE;")
                
                txt_acesso = f"Disponibilização do acesso aos beneficiários a partir de {data_acesso}." if data_acesso else "Disponibilização do acesso aos beneficiários a definir."
                pdf.bullet_point(txt_acesso)
                
                pdf.ln(2)
                txt_pag = f" O primeiro pagamento e o início das operações estão programados para {data_pagamento}." if data_pagamento else ""
                pdf.body_text(f"Obs.: Será realizada reunião de Kick Off para apresentação da equipe e entrega das plataformas após a assinatura do contrato.{txt_pag}")

                # 9. ISENÇÕES E CONDIÇÕES ESPECIAIS
                pdf.chapter_title("9. ISENÇÕES E CONDIÇÕES ESPECIAIS")
                pdf.body_text("Estão expressamente isentas de cobrança na plataforma principal:")
                pdf.bullet_point("Taxa de setup;")
                pdf.bullet_point("Taxa de implantação;")
                pdf.bullet_point("Taxa de personalização White Label;")
                pdf.bullet_point("Taxa de adesão.")

                # 10. SEGURANÇA DA INFORMAÇÃO E CONFORMIDADE
                pdf.chapter_title("10. SEGURANÇA DA INFORMAÇÃO E CONFORMIDADE")
                pdf.body_text("A LSX Medical assegura:")
                pdf.bullet_point("Conformidade com a LGPD, HIPAA e demais normas aplicáveis;")
                pdf.bullet_point("Criptografia de dados;")
                pdf.bullet_point("Controle de acesso e auditoria;")
                pdf.bullet_point("Integridade e rastreabilidade das informações clínicas.")

                # 11. VIGÊNCIA DAS CONDIÇÕES
                pdf.chapter_title("11. VIGÊNCIA DAS CONDIÇÕES")
                pdf.body_text("As condições comerciais e operacionais descritas neste Anexo:")
                pdf.bullet_point(f"Permanecerão válidas durante a vigência do contrato ({vigencia_contrato});")
                pdf.bullet_point("Estão condicionadas ao cumprimento do crescimento mínimo de vidas;")
                pdf.bullet_point("Não caracterizam desconto pontual, mas sim um modelo de parceria estratégica baseado em escala e previsibilidade.")

                # --- ASSINATURA ANCORADA AO FUNDO ---
                # Garante que a assinatura vá para uma nova página apenas se não houver espaço (230 de limite)
                if pdf.get_y() > 230:
                    pdf.add_page()
                
                # Empurra a assinatura para baixo, perto do rodapé (rodapé começa em -28)
                pdf.set_y(-60) 
                
                pdf.set_font('Arial', 'I', 9)
                pdf.set_text_color(100, 100, 100)
                pdf.cell(0, 5, limpa_texto("Este Anexo Comercial integra a proposta principal e consolida as condições para formalização contratual."), 0, 1, 'C')
                pdf.ln(5)
                
                y_ass = pdf.get_y()
                pdf.set_draw_color(*COR_PRIMARIA)
                pdf.line(70, y_ass, 140, y_ass)
                pdf.ln(3)
                
                pdf.set_font('Arial', 'B', 11)
                pdf.set_text_color(*COR_PRIMARIA)
                pdf.cell(0, 5, limpa_texto(nome_vendedor) if nome_vendedor else "Assinatura Comercial", 0, 1, 'C')
                
                if cargo_vendedor:
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

                nome_arquivo = f"Anexo_Comercial_LSX_{cliente_empresa.replace(' ', '_')}.pdf" if cliente_empresa else "Anexo_Comercial_LSX.pdf"
                pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace') 
                
                st.success("✅ Anexo Comercial Gerado com Sucesso!")
                st.download_button(
                    label="⬇️ BAIXAR ANEXO COMERCIAL (PDF)",
                    data=pdf_bytes,
                    file_name=nome_arquivo,
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")

if __name__ == "__main__":
    main()
