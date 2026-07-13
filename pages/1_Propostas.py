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
    if not texto:
        return ""
    replacements = {"•": "-", "–": "-", "—": "-", "“": '"', "”": '"', "\u2022": "-", "\u2028": "\n"}
    for char, rep in replacements.items():
        texto = str(texto).replace(char, rep)
    return texto.encode('latin-1', 'replace').decode('latin-1')


# ==============================================================================
# 2. MOTOR DE PRECIFICAÇÃO — VIDAS (TELEMEDICINA BASE / SEÇÃO 2)
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
# 2B. TABELAS DE PREÇO DOS DIFERENCIAIS ESTRATÉGICOS
# ==============================================================================

# --- Programa NR-1 / Suporte Psicossocial Corporativo ---
def calc_nr1_price(vidas):
    if vidas <= 10: return 18.90
    if vidas <= 20: return 16.90
    if vidas <= 30: return 14.90
    if vidas <= 40: return 12.90
    if vidas <= 49: return 10.90
    if vidas <= 50: return 9.90
    if vidas <= 150: return 8.90
    if vidas <= 200: return 7.90
    return 7.45

NR1_PACOTE1 = {"quinzenal": 58.11, "semanal": 93.87}   # Clínico Geral + Psicologia
NR1_PACOTE2 = {"quinzenal": 87.42, "semanal": 123.18}  # Psiquiatria + Psicologia

# --- Projeto Emagrecimento (Tirzepatida) — valor por vida ---
EMAGRECIMENTO_TABLE = [
    (50, 61.20), (60, 60.49), (80, 59.52), (100, 58.91), (150, 57.70),
    (200, 56.69), (300, 54.95), (400, 53.42), (10**9, 52.02)
]
def calc_emagrecimento_price(vidas):
    for limite, preco in EMAGRECIMENTO_TABLE:
        if vidas <= limite:
            return preco
    return EMAGRECIMENTO_TABLE[-1][1]

# --- Telemedicina em Canabidiol (CBD) ---
CBD_PRECO_CONSULTA = 49.90

# --- Projeto Remoção ---
REMOCAO_PRECO_CONSULTA = 29.90
REMOCAO_MINIMO_CONSULTAS = 100
REMOCAO_FEE_MENSAL = 2990.00

# --- Entrevista Qualificada Gravada ---
ENTREVISTA_OPCOES = {
    "Médico": {"preco": 49.90, "minimo": 100, "fee": 4990.00},
    "Técnico de Enfermagem / Enfermeiro": {"preco": 9.90, "minimo": 200, "fee": 1980.00},
}

# --- Projeto TEA — Planos ---
TEA_PLANOS = {
    "Plano Mensal — Manutenção (5 atendimentos/mês)": 373.00,
    "Plano Quinzenal — Intermediário (8 atendimentos/mês)": 548.00,
    "Plano Semanal — Intensivo (14 atendimentos/mês)": 898.00,
}

# --- Soluções LSX para Atenção Primária (Totem / Cabine / SSVV) ---
ATENCAO_PRIMARIA_SOLUCOES = {
    "Cabine 1x1 + Solução SSVV": {"locacao": 4147.00, "venda": 57720.00},
    "Cabine 1,5m x 2m + Solução SSVV": {"locacao": 5447.00, "venda": 71240.00},
    "Totem + Solução SSVV": {"locacao": 2535.00, "venda": 44070.00},
    "Solução SSVV (equipamentos de sinais vitais avulsos)": {"locacao": 1495.00, "venda": 29770.00},
}

# --- Contratação de Especialista por Volume Mínimo Inicial (genérico) ---
# Alternativa à consulta avulsa de mercado (R$150,00): ao contratar volume
# mínimo inicial de uma especialidade específica, o cliente acessa condições
# escalonadas de preço. Contratação à parte, complementar aos demais pacotes.
VOLUME_MINIMO_TABLE = [
    ("A partir de 50 consultas", 70.00, "Entrada acessível para novos contratos"),
    ("51 a 100 consultas", 68.50, "Redução de custo conforme crescimento inicial"),
    ("101 a 300 consultas", 65.90, "Economia significativa em operações em expansão"),
    ("301 a 500 consultas", 63.80, "Alta competitividade para grandes volumes"),
    ("Acima de 500 consultas", 61.60, "Máxima eficiência de custo na escala plena"),
]

AREAS_ESPECIFICAS_DISPONIVEIS = [
    "Psiquiatria", "Dermatologia", "Nutrição", "Cardiologia", "Endocrinologia",
    "Ortopedia", "Ginecologia", "Urologia", "Neurologia", "Geriatria",
    "Oftalmologia", "Otorrinolaringologia", "Outra (especificar)"
]

# --- App e Dashboard White Label (agora cobrado à parte) ---
APP_DASHBOARD_SETUP = 2500.00


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

    def price_table(self, headers, rows, col_widths=None):
        """Desenha uma tabela de preços genérica (usada por todos os diferenciais)."""
        if col_widths is None:
            n = len(headers)
            col_widths = [190 / n] * n

        # Cabeçalho
        self.set_font('Arial', 'B', 9)
        self.set_fill_color(*COR_PRIMARIA)
        self.set_text_color(255, 255, 255)
        for h, w in zip(headers, col_widths):
            self.cell(w, 7, limpa_texto(str(h)), 1, 0, 'C', fill=True)
        self.ln()

        # Linhas
        self.set_font('Arial', '', 9)
        self.set_text_color(50, 50, 50)
        fill = False
        for row in rows:
            self.set_fill_color(*COR_CINZA_CLARO) if fill else self.set_fill_color(255, 255, 255)
            for val, w in zip(row, col_widths):
                self.cell(w, 6.5, limpa_texto(str(val)), 1, 0, 'C', fill=True)
            self.ln()
            fill = not fill
        self.ln(3)


# ==============================================================================
# 4. APP STREAMLIT (LÓGICA E INTERFACE)
# ==============================================================================
def main():
    logo_padrao = "LOGO-LSX-Medical.png" if os.path.exists("LOGO-LSX-Medical.png") else None

    # --- SIDEBAR ---
    with st.sidebar:
        if logo_padrao:
            st.image(logo_padrao, use_container_width=True)
        else:
            st.title("LSX Config")

        st.markdown("### 👤 Dados do Emissor")
        nome_vendedor = st.text_input("Nome", value="Rauf Alencar")
        cargo_vendedor = st.text_input("Cargo", value="Gestor Comercial")
        telefone_vendedor = st.text_input("Telefone", value="(41) 99550-0770")
        email_vendedor = st.text_input("E-mail", value="contato@lsxmedical.com")

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

    # SEÇÃO 2: PRECIFICAÇÃO BASE (SIMPLES OU RAMPA)
    st.subheader("2. Dimensionamento e Precificação — Telemedicina Base")

    usar_rampa = st.checkbox("📈 Habilitar Rampa de Lançamento (Contrato com Escalonamento Mensal)")

    dados_rampa = None

    if usar_rampa:
        st.info("Preencha a tabela abaixo com a projeção mês a mês. O PDF gerará um cronograma financeiro completo.")

        meses_iniciais = [f"Mês {i}" for i in range(1, 13)]
        vidas_iniciais = [1000] * 12
        valores_iniciais = [5.90] * 12

        df_rampa = pd.DataFrame({
            "Período": meses_iniciais,
            "Qtd. Vidas": vidas_iniciais,
            "Valor por Vida (R$)": valores_iniciais
        })

        dados_rampa = st.data_editor(df_rampa, num_rows="dynamic", use_container_width=True, hide_index=True)

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

    # SEÇÃO 3: ESCOPO CLÍNICO CORE
    st.subheader("3. Configuração de Escopo e Diferenciais Estratégicos")

    c_scope1, c_scope2 = st.columns(2)

    with c_scope1:
        st.markdown("**Core Clínico (Incluso no Pronto Atendimento 24/7):**")
        st.checkbox("Clínico Geral 24/7", value=True, disabled=True)
        st.checkbox("Pediatria e Médico da Família", value=True)
        st.checkbox("Psicologia Orientativa (09h às 23h)", value=True)
        st.checkbox("Programa de Apoio ao Luto / Acolhimento", value=True)
        st.caption("App e Dashboard White Label agora é um item à parte — configure na coluna ao lado.")
        st.caption(
            "Rede ampliada disponível conforme diferenciais contratados: "
            "Psiquiatra, Psiquiatra Pediátrico/Neuropediatra, Nutricionista, "
            "Fonoaudiólogo e Fisioterapeuta."
        )

    # Lista que alimenta o PDF — cada item: titulo, descricao, tabela (headers/rows)
    diferenciais_selecionados = []

    with c_scope2:
        st.markdown("**Diferenciais B2B (marque para configurar cada um):**")

        # 1. Entrevista Qualificada Gravada
        inc_entrevista = st.checkbox("Projeto de Entrevista Qualificada Gravada")
        if inc_entrevista:
            with st.expander("⚙️ Configurar Entrevista Qualificada", expanded=True):
                tipo_prof = st.radio("Profissional entrevistador", list(ENTREVISTA_OPCOES.keys()), key="entrevista_tipo")
                cfg = ENTREVISTA_OPCOES[tipo_prof]
                st.info(f"Mínimo {cfg['minimo']} consultas a R$ {cfg['preco']:.2f} | Fee mensal: R$ {cfg['fee']:,.2f}")
                diferenciais_selecionados.append({
                    "titulo": "Projeto de Entrevista Qualificada Gravada",
                    "descricao": (
                        f"Formalização da Declaração de Saúde do beneficiário, conduzida por "
                        f"{tipo_prof.lower()}, com segurança jurídica, análise de risco assistencial "
                        f"e controle de sinistralidade — em conformidade com a legislação sanitária vigente."
                    ),
                    "tabela": {
                        "headers": ["Modalidade", "Valor/Consulta", "Volume Mínimo", "Fee Mensal"],
                        "rows": [[tipo_prof, f"R$ {cfg['preco']:.2f}", f"{cfg['minimo']} consultas", f"R$ {cfg['fee']:,.2f}"]]
                    }
                })

        # 2. Programa NR-1 / Suporte Psicossocial Corporativo
        inc_nr1 = st.checkbox("Programa de Suporte Psicossocial Corporativo (NR-1)")
        if inc_nr1:
            with st.expander("⚙️ Configurar Programa NR-1", expanded=True):
                vidas_nr1 = st.number_input("Número de beneficiários", min_value=1, value=50, key="nr1_vidas")
                preco_nr1 = calc_nr1_price(vidas_nr1)
                st.info(f"Valor sugerido: R$ {preco_nr1:.2f}/vida/mês (Total: R$ {preco_nr1 * vidas_nr1:,.2f}/mês)")
                inc_pacote1 = st.checkbox("Incluir Pacote 1 — Suporte Inicial (Clínico Geral + Psicologia), sob demanda", key="nr1_p1")
                inc_pacote2 = st.checkbox("Incluir Pacote 2 — Suporte Especializado (Psiquiatria + Psicologia), sob demanda", key="nr1_p2")

                tabela_rows = [["Programa Base NR-1 (mensal, por vida)", f"R$ {preco_nr1:.2f}"]]
                if inc_pacote1:
                    tabela_rows.append(["Pacote 1 Quinzenal — Clínico + Psicologia", f"R$ {NR1_PACOTE1['quinzenal']:.2f}"])
                    tabela_rows.append(["Pacote 1 Semanal — Clínico + Psicologia", f"R$ {NR1_PACOTE1['semanal']:.2f}"])
                if inc_pacote2:
                    tabela_rows.append(["Pacote 2 Quinzenal — Psiquiatria + Psicologia", f"R$ {NR1_PACOTE2['quinzenal']:.2f}"])
                    tabela_rows.append(["Pacote 2 Semanal — Psiquiatria + Psicologia", f"R$ {NR1_PACOTE2['semanal']:.2f}"])

                diferenciais_selecionados.append({
                    "titulo": "Programa de Suporte Psicossocial Corporativo (NR-1)",
                    "descricao": (
                        "Atendimento psicológico orientativo mensal a cada colaborador, com pesquisa "
                        "psicossocial inclusa (integrável ao PGR) e relatório mensal de indicadores em "
                        "conformidade com a LGPD. Pacotes de suporte clínico e psiquiátrico acionados "
                        "sob demanda, mediante indicação e aprovação da empresa."
                    ),
                    "tabela": {"headers": ["Serviço", "Valor / Colaborador"], "rows": tabela_rows}
                })

        # 3. Telemedicina em Canabidiol (CBD)
        inc_cbd = st.checkbox("Telemedicina em Canabidiol (CBD)")
        if inc_cbd:
            diferenciais_selecionados.append({
                "titulo": "Telemedicina em Canabidiol (CBD)",
                "descricao": (
                    "Avaliação médica e prescrição de canabidiol via telemedicina, em conformidade com "
                    "ANVISA e CFM, com acompanhamento contínuo (mensal, bimestral ou semestral conforme "
                    "evolução clínica) e cadastro automático via API."
                ),
                "tabela": {"headers": ["Serviço", "Valor"], "rows": [["Consulta avulsa de prescrição", f"R$ {CBD_PRECO_CONSULTA:.2f}"]]}
            })

        # 4. Projeto Emagrecimento (Tirzepatida)
        inc_emagrecimento = st.checkbox("Projeto Emagrecimento (Tirzepatida)")
        if inc_emagrecimento:
            with st.expander("⚙️ Configurar Projeto Emagrecimento", expanded=True):
                vidas_emag = st.number_input("Número de vidas estimado", min_value=1, value=50, key="emag_vidas")
                duracao_emag = st.selectbox("Duração do pacote", ["2 meses", "4 meses", "6 meses"], key="emag_duracao")
                preco_emag = calc_emagrecimento_price(vidas_emag)
                st.info(f"Valor sugerido: R$ {preco_emag:.2f}/vida (pacote {duracao_emag})")
                diferenciais_selecionados.append({
                    "titulo": "Projeto Emagrecimento (Tirzepatida)",
                    "descricao": (
                        f"Tratamento completo e integrado para pacientes em uso de Tirzepatida, com "
                        f"acompanhamento de Clínico Geral, Nutricionista e Psicólogo. Pacote de "
                        f"{duracao_emag}, com autoagendamento em todas as etapas."
                    ),
                    "tabela": {"headers": ["Vidas", "Valor por Vida", "Duração"], "rows": [[f"{vidas_emag}", f"R$ {preco_emag:.2f}", duracao_emag]]}
                })

        # 5. Soluções LSX para Atenção Primária (Totem/Cabine)
        inc_atencao_primaria = st.checkbox("Soluções LSX para Atenção Primária (Totem/Cabine)")
        if inc_atencao_primaria:
            with st.expander("⚙️ Configurar Soluções de Atenção Primária", expanded=True):
                solucoes_escolhidas = st.multiselect("Soluções desejadas", list(ATENCAO_PRIMARIA_SOLUCOES.keys()), key="ap_solucoes")
                modalidade_ap = st.radio("Modalidade", ["Locação Mensal", "Venda"], key="ap_modalidade")
                tabela_rows = []
                for sol in solucoes_escolhidas:
                    valores = ATENCAO_PRIMARIA_SOLUCOES[sol]
                    valor = valores["locacao"] if modalidade_ap == "Locação Mensal" else valores["venda"]
                    tabela_rows.append([sol, modalidade_ap, f"R$ {valor:,.2f}"])
                if tabela_rows:
                    diferenciais_selecionados.append({
                        "titulo": "Soluções LSX Medical para Atenção Primária",
                        "descricao": (
                            "Tecnologia 100% nacional (fabricação própria) para triagem autônoma e "
                            "telemedicina presencial — totens de sinais vitais e cabines de telemedicina, "
                            "com suporte técnico, treinamento e calibração periódica inclusos."
                        ),
                        "tabela": {"headers": ["Solução", "Modalidade", "Valor"], "rows": tabela_rows}
                    })
                else:
                    st.warning("Selecione ao menos uma solução para incluir na proposta.")

        # 6. Projeto Remoção
        inc_remocao = st.checkbox("Projeto Remoção (Barreira Assistencial)")
        if inc_remocao:
            diferenciais_selecionados.append({
                "titulo": "Projeto Remoção — Barreira Assistencial",
                "descricao": (
                    "Telemedicina como filtro clínico antes de qualquer acionamento de ambulância, "
                    "reduzindo remoções desnecessárias e custos operacionais. A decisão final sobre o "
                    "envio da ambulância é sempre baseada na avaliação médica da LSX Medical, com "
                    "respaldo técnico e legal ao contratante."
                ),
                "tabela": {
                    "headers": ["Item", "Valor"],
                    "rows": [
                        ["Consulta de triagem/remoção", f"R$ {REMOCAO_PRECO_CONSULTA:.2f}"],
                        ["Volume mínimo mensal", f"{REMOCAO_MINIMO_CONSULTAS} consultas"],
                        ["Fee mensal", f"R$ {REMOCAO_FEE_MENSAL:,.2f}"],
                    ]
                }
            })

        # 7. Projeto TEA
        inc_tea = st.checkbox("Projeto TEA — Acompanhamento Multidisciplinar")
        if inc_tea:
            with st.expander("⚙️ Configurar Projeto TEA", expanded=True):
                plano_tea = st.selectbox("Plano de acompanhamento", list(TEA_PLANOS.keys()), key="tea_plano")
                valor_tea = TEA_PLANOS[plano_tea]
                diferenciais_selecionados.append({
                    "titulo": "Projeto TEA — Planos de Acompanhamento Multidisciplinar",
                    "descricao": (
                        "Avaliação, diagnóstico e acompanhamento multidisciplinar 100% digital para "
                        "crianças com suspeita ou diagnóstico de TEA, com equipe de Clínico Geral, "
                        "Psiquiatra Pediátrico/Neuropediatra, Psicologia, Fonoaudiologia e Fisioterapia."
                    ),
                    "tabela": {"headers": ["Plano", "Valor Mensal"], "rows": [[plano_tea, f"R$ {valor_tea:,.2f}"]]}
                })

        # 8. Contratação de Especialista por Volume Mínimo Inicial (genérico)
        inc_volume_min = st.checkbox("Contratação de Especialista por Volume Mínimo Inicial")
        if inc_volume_min:
            with st.expander("⚙️ Configurar Especialidade por Volume", expanded=True):
                areas_selecionadas = st.multiselect(
                    "Áreas específicas contratadas (pode marcar mais de uma)",
                    AREAS_ESPECIFICAS_DISPONIVEIS,
                    key="vm_areas"
                )
                especialidade_custom = ""
                if "Outra (especificar)" in areas_selecionadas:
                    especialidade_custom = st.text_input(
                        "Especifique a(s) outra(s) área(s)",
                        placeholder="Ex: Reumatologia, Alergologia...",
                        key="vm_especialidade_custom"
                    )

                # Preview visual da tabela — igual à referência do cliente
                st.markdown("**Pré-visualização da tabela (entra assim no PDF):**")
                df_preview = pd.DataFrame(
                    [[f, f"R$ {p:.2f}", b] for f, p, b in VOLUME_MINIMO_TABLE],
                    columns=["Faixa de Volume Mensal", "Valor por Consulta", "Benefício"]
                )
                st.table(df_preview)

                areas_finais = [a for a in areas_selecionadas if a != "Outra (especificar)"]
                if especialidade_custom:
                    areas_finais += [a.strip() for a in especialidade_custom.split(",") if a.strip()]

                if areas_finais:
                    nome_areas = ", ".join(areas_finais)
                    diferenciais_selecionados.append({
                        "titulo": f"Contratação por Volume Mínimo Inicial — {nome_areas}",
                        "descricao": (
                            f"Alternativa à consulta avulsa de mercado (R$ 150,00): ao contratar um volume "
                            f"mínimo inicial nas áreas específicas de {nome_areas}, o contratante acessa "
                            f"condições escalonadas de preço. Contratação à parte, complementar aos demais "
                            f"pacotes desta proposta."
                        ),
                        "tabela": {
                            "headers": ["Faixa de Volume Mensal", "Valor por Consulta", "Benefício"],
                            "rows": [[f, f"R$ {p:.2f}", b] for f, p, b in VOLUME_MINIMO_TABLE]
                        }
                    })
                else:
                    st.warning("Selecione ao menos uma área específica para incluir esse item na proposta.")

        # 9. App e Dashboard White Label (agora item pago à parte)
        inc_app_dashboard = st.checkbox("App e Dashboard White Label (implantação)")
        if inc_app_dashboard:
            diferenciais_selecionados.append({
                "titulo": "App e Dashboard White Label",
                "descricao": (
                    "Aplicativo e painel white label com a identidade visual do contratante, incluindo "
                    "dados reais de uso, engajamento e performance da base de beneficiários. Item de "
                    "implantação, cobrado à parte do plano de telemedicina."
                ),
                "tabela": {
                    "headers": ["Item", "Valor"],
                    "rows": [["Implantação App e Dashboard White Label", f"R$ {APP_DASHBOARD_SETUP:,.2f}"]]
                }
            })

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
                if cliente_responsavel:
                    pdf.cell(0, 6, limpa_texto(f"Aos cuidados de: {cliente_responsavel}"), 0, 1)
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
                pdf.body_text(
                    "Rede médica ampliada disponível conforme os diferenciais contratados nesta proposta: "
                    "Psiquiatra, Psiquiatra Pediátrico/Neuropediatra, Nutricionista, Fonoaudiólogo e Fisioterapeuta."
                )

                pdf.sub_title("Saúde Mental e Apoio ao Luto")
                pdf.body_text("Atendimento de Psicologia Orientativa (das 09h às 23h). Como pilar central do projeto, estruturamos o programa de Apoio ao Luto e Acolhimento Familiar.")
                pdf.body_text("Sabemos que a dor não termina no momento da despedida — muitas vezes ela se intensifica nos dias seguintes. Oferecemos escuta qualificada e direcionamento emocional para as famílias num momento extremamente sensível, fortalecendo laços e gerando valor social à marca.")

                # --- DIFERENCIAIS ESTRATÉGICOS (dinâmico) ---
                if diferenciais_selecionados:
                    pdf.add_page()
                    pdf.chapter_title("4. SOLUÇÕES E DIFERENCIAIS CONTRATADOS")
                    for d in diferenciais_selecionados:
                        pdf.sub_title(d["titulo"])
                        pdf.body_text(d["descricao"])
                        if "tabela" in d:
                            pdf.price_table(d["tabela"]["headers"], d["tabela"]["rows"])
                    num_investimento = "5"
                    num_compliance = "6"
                else:
                    num_investimento = "4"
                    num_compliance = "5"

                # --- INVESTIMENTO E RAMPA ---
                pdf.add_page()
                pdf.chapter_title(f"{num_investimento}. MODELO DE INVESTIMENTO — TELEMEDICINA BASE")

                if usar_rampa and dados_rampa is not None:
                    pdf.body_text("Projeção de implantação com Rampa de Lançamento (Crescimento Escalonado):")
                    pdf.ln(3)

                    pdf.set_font('Arial', 'B', 10)
                    pdf.set_fill_color(*COR_PRIMARIA)
                    pdf.set_text_color(255, 255, 255)
                    pdf.cell(40, 8, 'Período', 1, 0, 'C', fill=True)
                    pdf.cell(50, 8, 'Vidas Estimadas', 1, 0, 'C', fill=True)
                    pdf.cell(50, 8, 'Valor Unitário', 1, 0, 'C', fill=True)
                    pdf.cell(50, 8, 'Faturamento Estimado', 1, 1, 'C', fill=True)

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

                # --- SEGURANÇA LEGAL ---
                pdf.ln(5)
                pdf.chapter_title(f"{num_compliance}. COMPROMISSO ÉTICO, SEGURANÇA E LEGALIDADE")
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
