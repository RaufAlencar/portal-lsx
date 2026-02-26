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
    "Geral / Corporativo": {
        "intro1": "A LSX Medical propõe transformar sua base de confiança em um cuidado contínuo de alto valor agregado. Nosso objetivo é estruturar e operar uma Clínica Digital de telemedicina totalmente personalizada, exclusiva e integralmente sob a marca {marca}.",
        "intro2": "Não se trata de uma plataforma genérica de mercado. Esta é uma operação desenhada para a realidade corporativa, focada em reduzir absenteísmo, otimizar custos de saúde e valorizar a sua marca empregadora perante colaboradores e clientes.",
        "titulo_mental": "Saúde Mental e Suporte Corporativo",
        "texto_mental": "Atendimento de Psicologia Orientativa (das 09h às 18h). Entendemos que a saúde mental é o maior desafio corporativo atual.\n\nDisponibilizamos suporte psicológico de rápido acesso para gerenciamento de estresse, ansiedade e prevenção de burnout, promovendo bem-estar e produtividade para os seus beneficiários."
    },
    "Funerárias / Assistência Familiar": {
        "intro1": "No setor de assistência familiar, o cuidado não termina com a despedida. A LSX Medical propõe transformar a {marca} em uma verdadeira provedora de saúde em vida, agregando valor tangível aos seus planos e aumentando a fidelização e retenção da sua carteira.",
        "intro2": "Desenhamos uma Clínica Digital 100% White Label. O grande diferencial desta proposta é o foco em Saúde Mental e Apoio ao Luto, oferecendo suporte contínuo para a família no momento em que ela mais precisa, consolidando a sua marca como um pilar de acolhimento.",
        "titulo_mental": "Saúde Mental e Apoio ao Luto",
        "texto_mental": "Atendimento de Psicologia Orientativa (das 09h às 18h). Como pilar central do projeto, estruturamos o programa de Apoio ao Luto e Acolhimento Familiar.\n\nSabemos que a dor não termina no momento da despedida — muitas vezes ela se intensifica nos dias seguintes. Oferecemos escuta qualificada e direcionamento emocional num momento extremamente sensível, fortalecendo laços e gerando valor social à marca."
    },
    "Cartões de Benefícios / Saúde": {
        "intro1": "Para aumentar o LTV (Life Time Value) e a atratividade do seu cartão, a LSX Medical oferece a infraestrutura completa para você operar a sua própria Clínica Digital de Telemedicina, fortalecendo o ecossistema da {marca}.",
        "intro2": "Entregue um benefício de uso imediato e alta percepção de valor. Uma solução 100% customizável, pronta para escalar suas vendas e gerar novas linhas de receita, sem a necessidade de investir em desenvolvimento tecnológico ou corpo clínico próprio.",
        "titulo_mental": "Saúde Mental de Acesso Rápido",
        "texto_mental": "Atendimento de Psicologia Orientativa (das 09h às 18h). Agregue alto valor percebido ao seu cartão entregando cuidado emocional.\n\nNossos profissionais estão disponíveis para triagem e orientação em casos de ansiedade, crises pontuais e conflitos familiares. Um benefício que gera uso recorrente e fideliza o usuário ao seu produto."
    },
    "Hospitais, Clínicas e Planos de Saúde": {
        "intro1": "A LSX Medical atua como o braço tecnológico e de retaguarda médica da {marca}. Nossa solução de Clínica Digital visa otimizar sua operação, desafogar prontos-socorros físicos e expandir sua capilaridade de atendimento.",
        "intro2": "Com protocolos integrados e fluxos de triagem digital (Pronto Atendimento Virtual), reduzimos custos operacionais e sinistralidade, garantindo a excelência do cuidado primário e o direcionamento inteligente de casos de alta complexidade para a sua rede física.",
        "titulo_mental": "Triagem e Orientação Psicológica",
        "texto_mental": "Atendimento de Psicologia Orientativa (das 09h às 18h). Atua como um importante filtro para a rede presencial.\n\nRealizamos o acolhimento, escuta qualificada e encaminhamento assertivo. Ideal para pacientes com quadros leves, evitando idas desnecessárias à emergência e oferecendo conforto e comodidade diretamente pelo aplicativo."
    },
    "Varejo e Grandes Redes": {
        "intro1": "O varejo moderno exige inovação na retenção de clientes e na monetização da base. A LSX propõe que a {marca} ofereça saúde de qualidade como um serviço financeiro e de fidelidade (Health as a Service).",
        "intro2": "Com nossa plataforma White Label, você entrega um benefício percebido como essencial, aumentando o engajamento do cliente com o seu ecossistema, gerando recorrência e abrindo uma nova frente de faturamento altamente rentável.",
        "titulo_mental": "Bem-Estar e Psicologia Orientativa",
        "texto_mental": "Atendimento de Psicologia Orientativa (das 09h às 18h). Diferencie o seu programa de fidelidade entregando acolhimento.\n\nOferecemos acesso rápido a profissionais de saúde mental para orientações gerais. Um serviço moderno que conecta a sua marca diretamente ao cuidado pessoal do seu cliente."
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
        self.set_auto_page_break(auto=True, margin=35) 

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

    st.subheader("1. Dados do Cliente e Inteligência Comercial")
    col1, col2, col3 = st.columns([2, 1, 1])
    cliente_empresa = col1.text_input("Razão Social / Empresa", placeholder="Ex: Grupo UMUPREV")
    cliente_responsavel = col2.text_input("Nome do Responsável", placeholder="Ex: João Silva")
    segmento_selecionado = col3.selectbox("Segmento de Atuação", list(TEXTOS_SEGMENTOS.keys()))
    
    nome_fantasia_cliente = cliente_empresa if cliente_empresa else "Sua Empresa"

    st.markdown("---")
    
    st.subheader("2. Dimensionamento e Precificação")
    col_vig, col_rampa = st.columns([1, 2])
    vigencia_contrato = col_vig.radio("Vigência do Contrato", ["12 Meses", "24 Meses"], index=1)
    
    usar_rampa = col_rampa.checkbox("📈 Habilitar Cronograma de Implantação (Rampa de Crescimento)")
    dados_rampa = None 
    
    if usar_rampa:
        st.info("Preencha a expectativa de crescimento (Adicione ou remova linhas conforme os meses de implantação). A política de descontos progressivos por volume será gerada automaticamente.")
        meses_iniciais = [f"Mês {i}" for i in range(1, 4)] 
        vidas_iniciais = [1000, 3000, 5000]
        valores_iniciais = [calcular_preco_sugerido(v) for v in vidas_iniciais]
        
        df_rampa = pd.DataFrame({
            "Período": meses_iniciais, "Qtd. Vidas (Meta)": vidas_iniciais, "Valor por Vida (R$)": valores_iniciais
        })
        dados_rampa = st.data_editor(df_rampa, num_rows="dynamic", use_container_width=True, hide_index=True)
        dados_rampa = dados_rampa.fillna(0)
        
        try:
            qtd_vidas = int(dados_rampa["Qtd. Vidas (Meta)"].max())
        except:
            qtd_vidas = 1000
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
                <h3 style="margin:0; color: #001E50;">Faturamento Base: R$ {total_mensal:,.2f} /mês</h3>
                <p style="margin:0; color: #555;">Iniciando com {qtd_vidas} vidas a R$ {valor_unitario:.2f}. O cliente terá acesso automático a descontos se ultrapassar esse volume.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
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
        inc_protocolos = st.checkbox("Protocolos clínicos corporativos", value=False)
        inc_cabine = st.checkbox("Cabine Física de Telemedicina", value=False)
    
    obs_comerciais = st.text_area("Observações Comerciais (Ex: Carência, Setup de Implantação)", height=80)

    st.markdown("---")
    submit_btn = st.button("GERAR PROPOSTA ENTERPRISE (PDF) 🚀")

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
                
                # --- INTRODUÇÃO DINÂMICA ---
                copy_intro = TEXTOS_SEGMENTOS[segmento_selecionado]
                
                pdf.chapter_title(f"1. A CLÍNICA DIGITAL {nome_fantasia_cliente.upper()}")
                pdf.body_text(copy_intro["intro1"].replace("{marca}", nome_fantasia_cliente))
                pdf.body_text(copy_intro["intro2"])

                # --- JORNADA E GATILHOS DE GRATUIDADE ---
                pdf.chapter_title("2. TECNOLOGIA E IMPLANTAÇÃO (BÔNUS 100% INCLUSO)")
                pdf.body_text("Para viabilizar uma parceria de longo prazo e garantir tração rápida, a LSX Medical subsidia integralmente o custo de tecnologia. Você terá ISENÇÃO TOTAL de Taxa de Setup. O pacote inclui:")
                pdf.bullet_point(f"Desenvolvimento White Label: Aplicativo e Plataforma completa com a identidade, nome e cores da {nome_fantasia_cliente}.")
                pdf.bullet_point("Helpdesk e Treinamento: Corpo clínico e atendimento atuando como extensão oficial da sua equipe sem custo extra.")
                pdf.bullet_point(f"Documentos Oficiais: Atestados, receituários ICP-Brasil e exames emitidos com a marca {nome_fantasia_cliente}.")
                pdf.bullet_point("Dashboard Exclusivo: Painel corporativo com dados reais de uso, engajamento e performance da base.")

                # --- ESCOPO CORE ---
                if pdf.get_y() > 190: pdf.add_page()
                
                pdf.chapter_title("3. ESCOPO MÉDICO E ASSISTENCIAL")
                pdf.sub_title("Pronto Atendimento 24h / 7 Dias")
                pdf.body_text("Acesso imediato e ilimitado para triagem, diagnóstico e prescrição. Corpo clínico composto por:")
                pdf.bullet_point("Clínico Geral")
                pdf.bullet_point("Pediatra")
                pdf.bullet_point("Médico da Família")

                # SAÚDE MENTAL DINÂMICA
                pdf.sub_title(copy_intro["titulo_mental"])
                for paragrafo in copy_intro["texto_mental"].split("\n\n"):
                    pdf.body_text(paragrafo)

                # --- DIFERENCIAIS ---
                diferenciais = []
                if inc_televet: diferenciais.append("Televeterinária (cuidado ampliado para o bem-estar de toda a família).")
                if inc_entrevista: diferenciais.append("Projeto de Entrevista Qualificada (inteligência de dados da base).")
                if inc_nr1: diferenciais.append("Programa de Regulamentação NR-1 (oportunidade de escala B2B).")
                if inc_protocolos: diferenciais.append("Protocolos clínicos estruturados para demandas corporativas/específicas.")
                if inc_cabine: diferenciais.append("Fornecimento de Cabine Física de Telemedicina para alocação presencial.")

                if diferenciais:
                    if pdf.get_y() > 220: pdf.add_page()
                    pdf.ln(3)
                    pdf.sub_title("Diferenciais Estratégicos Agregados")
                    for d in diferenciais:
                        pdf.bullet_point(d)

                # --- INVESTIMENTO E POLÍTICA DE UPSELL ---
                pdf.add_page() 
                pdf.chapter_title("4. MODELO DE INVESTIMENTO E ESCALA")
                
                # Parte 1: Implantação / Fixa
                if usar_rampa and dados_rampa is not None:
                    pdf.body_text("Cronograma de Implantação (Rampa de Lançamento):")
                    pdf.ln(3)
                    
                    pdf.set_font('Arial', 'B', 10)
                    pdf.set_fill_color(*COR_PRIMARIA)
                    pdf.set_text_color(255, 255, 255)
                    pdf.cell(50, 8, 'Período', 1, 0, 'C', fill=True)
                    pdf.cell(60, 8, 'Vidas Ativas (Meta)', 1, 0, 'C', fill=True)
                    pdf.cell(60, 8, 'Valor Unitário Aplicado', 1, 1, 'C', fill=True)

                    pdf.set_font('Arial', '', 10)
                    pdf.set_text_color(50, 50, 50)
                    
                    for index, row in dados_rampa.iterrows():
                        mes = str(row['Período'])
                        try:
                            vidas = int(row['Qtd. Vidas (Meta)'])
                            valor = float(row['Valor por Vida (R$)'])
                        except:
                            vidas, valor = 0, 0.0
                            
                        pdf.cell(50, 8, limpa_texto(mes), 1, 0, 'C')
                        pdf.cell(60, 8, f"{vidas:,}", 1, 0, 'C')
                        pdf.cell(60, 8, f"R$ {valor:,.2f}", 1, 1, 'C')
                        
                else:
                    pdf.set_fill_color(*COR_CINZA_CLARO)
                    pdf.rect(10, pdf.get_y(), 190, 40, 'F')
                    pdf.set_y(pdf.get_y() + 5)
                    
                    pdf.set_font('Arial', 'B', 12)
                    pdf.set_text_color(*COR_PRIMARIA)
                    pdf.cell(95, 10, limpa_texto("VOLUME INICIAL CONTRATADO"), 0, 0, 'C')
                    pdf.cell(95, 10, limpa_texto("VALOR MENSAL POR VIDA"), 0, 1, 'C')
                    
                    pdf.set_font('Arial', '', 14)
                    pdf.set_text_color(50, 50, 50)
                    pdf.cell(95, 10, limpa_texto(f"{qtd_vidas} Beneficiários ativos"), 0, 0, 'C')
                    
                    pdf.set_font('Arial', 'B', 22)
                    pdf.set_text_color(*COR_SECUNDARIA) 
                    pdf.cell(95, 10, f"R$ {valor_unitario:,.2f}", 0, 1, 'C')
                    pdf.ln(12)

                # Parte 2: A Tabela Progressiva
                pdf.ln(8)
                pdf.sub_title("Política de Crescimento e Upsell (Descontos Progressivos):")
                pdf.body_text("Nossa parceria foi desenhada para escalar com você. Não há limite de crescimento. Conforme a base de usuários aumenta, o custo unitário da operação diminui automaticamente, aumentando sua margem de lucro:")
                
                pdf.ln(2)
                pdf.set_font('Arial', 'B', 9)
                pdf.set_fill_color(240, 240, 240)
                pdf.set_text_color(*COR_PRIMARIA)
                pdf.cell(85, 6, 'Volume de Vidas Ativas', 1, 0, 'C', fill=True)
                pdf.cell(85, 6, 'Valor Unitário (Desconto Progressivo)', 1, 1, 'C', fill=True)
                
                pdf.set_font('Arial', '', 9)
                pdf.set_text_color(50, 50, 50)
                
                faixas_crescimento = [3000, 6000, 9000, 15000, 25000, 35000]
                faixas_para_mostrar = [f for f in faixas_crescimento if f > qtd_vidas]
                
                if not faixas_para_mostrar: 
                    faixas_para_mostrar = [qtd_vidas + 5000, qtd_vidas + 15000] 
                    
                for limite in faixas_para_mostrar:
                    preco_faixa = calcular_preco_sugerido(limite)
                    pdf.cell(85, 6, f"Acima de {limite:,} vidas", 1, 0, 'C')
                    pdf.cell(85, 6, f"R$ {preco_faixa:,.2f}", 1, 1, 'C')
                
                pdf.ln(8)
                pdf.sub_title("Diretrizes Comerciais:")
                pdf.bullet_point(f"Vigência Contratual: {vigencia_contrato} (Período mínimo para sustentação da tabela de preços).")
                pdf.bullet_point("Reajuste: Anual com base no índice IPCA.")
                # FATURAMENTO CORRIGIDO:
                pdf.bullet_point("Faturamento: Cobrança fixa mensal baseada na quantidade de vidas contratada (faixa atual), com liberdade para escalar.")
                if obs_comerciais:
                    pdf.bullet_point(f"Observações: {obs_comerciais}")

                # --- COMPLIANCE ---
                if pdf.get_y() > 190: 
                    pdf.add_page()
                else:
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

                # --- ASSINATURA ---
                if pdf.get_y() > 220:
                    pdf.add_page()
                else:
                    pdf.ln(20) 
                
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
