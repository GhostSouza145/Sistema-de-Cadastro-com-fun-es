"""
Sistema de Biblioteca com Interface Gráfica
Autor: [Seu Nome Completo]
Tema: Sistema de Biblioteca com GUI
Turma: [Sua Turma]
Data: [Data de Entrega]
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Instalar customtkinter se não estiver instalado
# pip install customtkinter
import customtkinter as ctk

# Configurar aparência
ctk.set_appearance_mode("Dark")  # Modos: "Dark", "Light", "System"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

class SistemaBiblioteca:
    def __init__(self):
        self.livros = []
        self.proximo_id = 1
        self.carregar_dados()
        self.inicializar_gui()
    
    def carregar_dados(self):
        """Carrega dados do arquivo JSON se existir"""
        try:
            if os.path.exists("biblioteca_data.json"):
                with open("biblioteca_data.json", 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.livros = dados.get('livros', [])
                    self.proximo_id = dados.get('proximo_id', 1)
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
    
    def salvar_dados(self):
        """Salva dados no arquivo JSON"""
        try:
            dados = {
                'livros': self.livros,
                'proximo_id': self.proximo_id
            }
            with open("biblioteca_data.json", 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False
    
    def inicializar_gui(self):
        """Inicializa a interface gráfica"""
        self.root = ctk.CTk()
        self.root.title("Sistema de Biblioteca - Biblioteca Moderna")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Configurar grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.criar_sidebar()
        self.criar_area_principal()
        self.atualizar_estatisticas()
    
    def criar_sidebar(self):
        """Cria a barra lateral com menu"""
        sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(8, weight=1)
        
        # Logo e título
        logo_label = ctk.CTkLabel(
            sidebar, 
            text="📚 Biblioteca", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        logo_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Botões do menu
        botoes_menu = [
            ("📖 Cadastrar Livro", self.mostrar_cadastro),
            ("📚 Listar Livros", self.mostrar_listagem),
            ("🔍 Buscar Livro", self.mostrar_busca),
            ("✏️ Atualizar Livro", self.mostrar_atualizacao),
            ("🗑️ Remover Livro", self.mostrar_remocao),
            ("📋 Empréstimos", self.mostrar_emprestimos),
            ("📊 Estatísticas", self.mostrar_estatisticas),
        ]
        
        for i, (texto, comando) in enumerate(botoes_menu, 1):
            btn = ctk.CTkButton(
                sidebar, 
                text=texto,
                command=comando,
                font=ctk.CTkFont(size=14),
                height=40,
                fg_color="transparent",
                hover_color=("gray70", "gray30")
            )
            btn.grid(row=i, column=0, padx=20, pady=5, sticky="ew")
        
        # Botão sair
        sair_btn = ctk.CTkButton(
            sidebar, 
            text="🚪 Sair",
            command=self.sair,
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color="#d9534f",
            hover_color="#c9302c"
        )
        sair_btn.grid(row=9, column=0, padx=20, pady=20, sticky="ew")
    
    def criar_area_principal(self):
        """Cria a área principal onde o conteúdo será exibido"""
        self.area_principal = ctk.CTkFrame(self.root, corner_radius=10)
        self.area_principal.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.area_principal.grid_columnconfigure(0, weight=1)
        self.area_principal.grid_rowconfigure(1, weight=1)
        
        # Título da área principal
        self.titulo_area = ctk.CTkLabel(
            self.area_principal, 
            text="Bem-vindo ao Sistema de Biblioteca",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.titulo_area.grid(row=0, column=0, padx=20, pady=20)
        
        # Frame de conteúdo
        self.frame_conteudo = ctk.CTkFrame(self.area_principal)
        self.frame_conteudo.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.frame_conteudo.grid_columnconfigure(0, weight=1)
        self.frame_conteudo.grid_rowconfigure(0, weight=1)
        
        # Tela inicial
        self.mostrar_tela_inicial()
    
    def mostrar_tela_inicial(self):
        """Mostra a tela inicial"""
        self.limpar_conteudo()
        
        conteudo = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        conteudo.grid(row=0, column=0, sticky="nsew")
        conteudo.grid_columnconfigure(0, weight=1)
        
        # Mensagem de boas-vindas
        welcome_text = """
        🏛️ BEM-VINDO À BIBLIOTECA MODERNA
        
        Um sistema completo para gerenciamento de acervo bibliográfico.
        
        📈 Estatísticas atuais:
        """
        
        welcome_label = ctk.CTkLabel(
            conteudo, 
            text=welcome_text,
            font=ctk.CTkFont(size=16),
            justify="center"
        )
        welcome_label.grid(row=0, column=0, pady=20)
        
        # Frame de estatísticas rápidas
        stats_frame = ctk.CTkFrame(conteudo)
        stats_frame.grid(row=1, column=0, pady=20, padx=100, sticky="ew")
        
        self.stats_labels = {}
        stats_data = [
            ("📚 Total de Livros", "total_livros"),
            ("✅ Disponíveis", "disponiveis"),
            ("❌ Emprestados", "emprestados"),
            ("💰 Preço Médio", "preco_medio")
        ]
        
        for i, (texto, chave) in enumerate(stats_data):
            label_frame = ctk.CTkFrame(stats_frame, height=80)
            label_frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            label_frame.grid_propagate(False)
            
            title_label = ctk.CTkLabel(
                label_frame, 
                text=texto,
                font=ctk.CTkFont(size=12)
            )
            title_label.pack(pady=(10, 5))
            
            value_label = ctk.CTkLabel(
                label_frame, 
                text="0",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            value_label.pack(pady=(0, 10))
            
            self.stats_labels[chave] = value_label
        
        stats_frame.grid_columnconfigure((0,1,2,3), weight=1)
    
    def mostrar_cadastro(self):
        """Mostra o formulário de cadastro"""
        self.limpar_conteudo()
        self.titulo_area.configure(text="📖 Cadastrar Novo Livro")
        
        form_frame = ctk.CTkFrame(self.frame_conteudo)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Campos do formulário
        campos = [
            ("Título*", "entry_titulo"),
            ("Autor*", "entry_autor"),
            ("Ano de Publicação*", "entry_ano"),
            ("Gênero", "entry_genero"),
            ("Preço (R$)", "entry_preco")
        ]
        
        self.entries = {}
        
        for i, (label, key) in enumerate(campos):
            lbl = ctk.CTkLabel(form_frame, text=label, font=ctk.CTkFont(size=14))
            lbl.grid(row=i, column=0, padx=20, pady=10, sticky="w")
            
            entry = ctk.CTkEntry(form_frame, font=ctk.CTkFont(size=14), height=35)
            entry.grid(row=i, column=1, padx=20, pady=10, sticky="ew")
            self.entries[key] = entry
        
        # Botões
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=len(campos), column=0, columnspan=2, pady=30)
        
        ctk.CTkButton(
            btn_frame, 
            text="💾 Salvar Livro",
            command=self.salvar_livro,
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color="#5cb85c",
            hover_color="#4cae4c"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame, 
            text="🔄 Limpar",
            command=self.limpar_formulario,
            font=ctk.CTkFont(size=14),
            height=40
        ).pack(side="left", padx=10)
    
    def mostrar_listagem(self):
        """Mostra a listagem de livros"""
        self.limpar_conteudo()
        self.titulo_area.configure(text="📚 Lista de Livros")
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.frame_conteudo)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Frame de controles
        controles_frame = ctk.CTkFrame(main_frame)
        controles_frame.grid(row=0, column=0, sticky="ew", pady=10)
        
        ctk.CTkLabel(
            controles_frame, 
            text="Filtrar por:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.filtro_var = ctk.StringVar(value="Todos")
        filtro_combo = ctk.CTkComboBox(
            controles_frame,
            values=["Todos", "Disponíveis", "Emprestados"],
            variable=self.filtro_var,
            command=self.filtrar_lista,
            width=150
        )
        filtro_combo.pack(side="left", padx=10)
        
        # Treeview para listagem
        tree_frame = ctk.CTkFrame(main_frame)
        tree_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Criar treeview com estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=('Arial', 11), rowheight=25)
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
        
        columns = ("ID", "Título", "Autor", "Ano", "Gênero", "Preço", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        col_widths = [50, 250, 150, 80, 120, 80, 120]
        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.atualizar_listagem()
    
    def mostrar_busca(self):
        """Mostra a tela de busca"""
        self.limpar_conteudo()
        self.titulo_area.configure(text="🔍 Buscar Livros")
        
        main_frame = ctk.CTkFrame(self.frame_conteudo)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Campo de busca
        ctk.CTkLabel(
            main_frame, 
            text="Digite o título ou autor para buscar:",
            font=ctk.CTkFont(size=14)
        ).grid(row=0, column=0, pady=10, sticky="w")
        
        self.entry_busca = ctk.CTkEntry(main_frame, font=ctk.CTkFont(size=14), height=35)
        self.entry_busca.grid(row=1, column=0, pady=10, sticky="ew")
        self.entry_busca.bind("<KeyRelease>", self.realizar_busca)
        
        # Treeview para resultados
        tree_frame = ctk.CTkFrame(main_frame)
        tree_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        self.tree_busca = ttk.Treeview(
            tree_frame, 
            columns=("ID", "Título", "Autor", "Ano", "Status"), 
            show="headings",
            height=10
        )
        
        for col, width in zip(("ID", "Título", "Autor", "Ano", "Status"), [50, 250, 150, 80, 120]):
            self.tree_busca.heading(col, text=col)
            self.tree_busca.column(col, width=width)
        
        scrollbar_busca = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_busca.yview)
        self.tree_busca.configure(yscrollcommand=scrollbar_busca.set)
        
        self.tree_busca.grid(row=0, column=0, sticky="nsew")
        scrollbar_busca.grid(row=0, column=1, sticky="ns")
    
    def mostrar_atualizacao(self):
        """Mostra a tela de atualização"""
        self.mostrar_listagem()
        self.titulo_area.configure(text="✏️ Atualizar Livro - Selecione um livro da lista")
        
        # Adicionar botão de atualização
        btn_frame = ctk.CTkFrame(self.frame_conteudo)
        btn_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Atualizar Livro Selecionado",
            command=self.abrir_janela_atualizacao,
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color="#f0ad4e",
            hover_color="#eea236"
        ).pack(pady=10)
    
    def mostrar_remocao(self):
        """Mostra a tela de remoção"""
        self.mostrar_listagem()
        self.titulo_area.configure(text="🗑️ Remover Livro - Selecione um livro da lista")
        
        btn_frame = ctk.CTkFrame(self.frame_conteudo)
        btn_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="❌ Remover Livro Selecionado",
            command=self.remover_livro_selecionado,
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color="#d9534f",
            hover_color="#c9302c"
        ).pack(pady=10)
    
    def mostrar_emprestimos(self):
        """Mostra a tela de gerenciamento de empréstimos"""
        self.limpar_conteudo()
        self.titulo_area.configure(text="📋 Gerenciar Empréstimos")
        
        main_frame = ctk.CTkFrame(self.frame_conteudo)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Frame de controles
        controles_frame = ctk.CTkFrame(main_frame)
        controles_frame.grid(row=0, column=0, sticky="ew", pady=10)
        
        ctk.CTkLabel(
            controles_frame,
            text="Selecione um livro para gerenciar empréstimo:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        # Treeview para livros
        tree_frame = ctk.CTkFrame(main_frame)
        tree_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        self.tree_emprestimos = ttk.Treeview(
            tree_frame,
            columns=("ID", "Título", "Autor", "Status", "Emprestado Para"),
            show="headings",
            height=12
        )
        
        for col, width in zip(("ID", "Título", "Autor", "Status", "Emprestado Para"), [50, 250, 150, 120, 150]):
            self.tree_emprestimos.heading(col, text=col)
            self.tree_emprestimos.column(col, width=width)
        
        scrollbar_emp = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_emprestimos.yview)
        self.tree_emprestimos.configure(yscrollcommand=scrollbar_emp.set)
        
        self.tree_emprestimos.grid(row=0, column=0, sticky="nsew")
        scrollbar_emp.grid(row=0, column=1, sticky="ns")
        
        # Frame de botões
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.grid(row=2, column=0, sticky="ew", pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="📥 Emprestar Livro",
            command=self.emprestar_livro,
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color="#5cb85c"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="📤 Devolver Livro",
            command=self.devolver_livro,
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color="#5bc0de"
        ).pack(side="left", padx=10)
        
        self.atualizar_lista_emprestimos()
    
    def mostrar_estatisticas(self):
        """Mostra a tela de estatísticas"""
        self.limpar_conteudo()
        self.titulo_area.configure(text="📊 Estatísticas da Biblioteca")
        
        stats_frame = ctk.CTkFrame(self.frame_conteudo)
        stats_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        stats_frame.grid_columnconfigure((0,1,2), weight=1)
        stats_frame.grid_rowconfigure((0,1), weight=1)
        
        # Criar cards de estatísticas
        estatisticas = self.calcular_estatisticas()
        
        cards_data = [
            ("📚 Total de Livros", estatisticas['total'], "#17a2b8"),
            ("✅ Disponíveis", estatisticas['disponiveis'], "#28a745"),
            ("❌ Emprestados", estatisticas['emprestados'], "#dc3545"),
            ("💰 Preço Médio", f"R$ {estatisticas['preco_medio']:.2f}", "#ffc107"),
            ("📅 Ano Mais Recente", estatisticas['ano_recente'], "#6f42c1"),
            ("📅 Ano Mais Antigo", estatisticas['ano_antigo'], "#fd7e14"),
        ]
        
        for i, (titulo, valor, cor) in enumerate(cards_data):
            row = i // 3
            col = i % 3
            
            card = ctk.CTkFrame(stats_frame, fg_color=cor, corner_radius=15)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card.grid_propagate(False)
            card.configure(width=200, height=120)
            
            ctk.CTkLabel(
                card,
                text=titulo,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="white"
            ).pack(pady=(15, 5))
            
            ctk.CTkLabel(
                card,
                text=str(valor),
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="white"
            ).pack(pady=5)
    
    # Métodos funcionais
    def salvar_livro(self):
        """Salva um novo livro"""
        try:
            titulo = self.entries['entry_titulo'].get().strip()
            autor = self.entries['entry_autor'].get().strip()
            ano = self.entries['entry_ano'].get().strip()
            genero = self.entries['entry_genero'].get().strip() or "Não especificado"
            preco = self.entries['entry_preco'].get().strip() or "0"
            
            # Validações
            if not titulo or not autor or not ano:
                messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios (*)")
                return
            
            if not ano.isdigit() or len(ano) != 4:
                messagebox.showwarning("Atenção", "Ano deve ter 4 dígitos")
                return
            
            try:
                preco_valor = float(preco) if preco else 0.0
                if preco_valor < 0:
                    messagebox.showwarning("Atenção", "Preço não pode ser negativo")
                    return
            except ValueError:
                messagebox.showwarning("Atenção", "Preço deve ser um número válido")
                return
            
            # Verificar duplicata
            for livro in self.livros:
                if (livro['titulo'].lower() == titulo.lower() and 
                    livro['autor'].lower() == autor.lower()):
                    messagebox.showwarning("Atenção", "Este livro já está cadastrado!")
                    return
            
            # Criar livro
            livro = {
                'id': self.proximo_id,
                'titulo': titulo,
                'autor': autor,
                'ano': int(ano),
                'genero': genero,
                'preco': preco_valor,
                'disponivel': True,
                'emprestado_para': ""
            }
            
            self.livros.append(livro)
            self.proximo_id += 1
            
            if self.salvar_dados():
                self.limpar_formulario()
                self.atualizar_estatisticas()
                messagebox.showinfo("Sucesso", f"Livro '{titulo}' cadastrado com ID {livro['id']}!")
            else:
                messagebox.showerror("Erro", "Erro ao salvar dados no arquivo")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar livro: {str(e)}")
    
    def atualizar_listagem(self, filtro=None):
        """Atualiza a listagem de livros"""
        if not hasattr(self, 'tree') or not self.tree.winfo_exists():
            return
            
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if filtro is None:
            filtro = self.filtro_var.get() if hasattr(self, 'filtro_var') else "Todos"
        
        livros_filtrados = self.livros
        
        if filtro == "Disponíveis":
            livros_filtrados = [l for l in self.livros if l['disponivel']]
        elif filtro == "Emprestados":
            livros_filtrados = [l for l in self.livros if not l['disponivel']]
        
        for livro in sorted(livros_filtrados, key=lambda x: x['titulo']):
            status = "✅ Disponível" if livro['disponivel'] else f"❌ Emprestado"
            self.tree.insert("", "end", values=(
                livro['id'],
                livro['titulo'],
                livro['autor'],
                livro['ano'],
                livro['genero'],
                f"R$ {livro['preco']:.2f}",
                status
            ))
    
    def realizar_busca(self, event=None):
        """Realiza busca em tempo real"""
        termo = self.entry_busca.get().strip().lower()
        
        if not hasattr(self, 'tree_busca') or not self.tree_busca.winfo_exists():
            return
            
        for item in self.tree_busca.get_children():
            self.tree_busca.delete(item)
        
        if termo:
            resultados = []
            for livro in self.livros:
                if (termo in livro['titulo'].lower() or 
                    termo in livro['autor'].lower()):
                    resultados.append(livro)
            
            for livro in resultados:
                status = "✅ Disponível" if livro['disponivel'] else "❌ Emprestado"
                self.tree_busca.insert("", "end", values=(
                    livro['id'],
                    livro['titulo'],
                    livro['autor'],
                    livro['ano'],
                    status
                ))
    
    def abrir_janela_atualizacao(self):
        """Abre janela para atualizar livro selecionado"""
        if not hasattr(self, 'tree') or not self.tree.winfo_exists():
            messagebox.showwarning("Atenção", "Lista não disponível")
            return
            
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um livro para atualizar")
            return
        
        item = self.tree.item(selecionado[0])
        livro_id = item['values'][0]
        
        livro = next((l for l in self.livros if l['id'] == livro_id), None)
        if not livro:
            messagebox.showerror("Erro", "Livro não encontrado")
            return
        
        # Criar janela de atualização
        janela = ctk.CTkToplevel(self.root)
        janela.title("Atualizar Livro")
        janela.geometry("500x400")
        janela.transient(self.root)
        janela.grab_set()
        
        ctk.CTkLabel(
            janela,
            text=f"Atualizar: {livro['titulo']}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        form_frame = ctk.CTkFrame(janela)
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)
        form_frame.grid_columnconfigure(1, weight=1)
        
        campos = [
            ("Título", livro['titulo']),
            ("Autor", livro['autor']),
            ("Ano", str(livro['ano'])),
            ("Gênero", livro['genero']),
            ("Preço", str(livro['preco']))
        ]
        
        entries_upd = {}
        
        for i, (label, valor) in enumerate(campos):
            lbl = ctk.CTkLabel(form_frame, text=label, font=ctk.CTkFont(size=14))
            lbl.grid(row=i, column=0, padx=10, pady=10, sticky="w")
            
            entry = ctk.CTkEntry(form_frame, font=ctk.CTkFont(size=14), height=35)
            entry.insert(0, valor)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
            entries_upd[label.lower()] = entry
        
        def atualizar():
            try:
                livro['titulo'] = entries_upd['título'].get().strip()
                livro['autor'] = entries_upd['autor'].get().strip()
                livro['ano'] = int(entries_upd['ano'].get().strip())
                livro['genero'] = entries_upd['gênero'].get().strip()
                livro['preco'] = float(entries_upd['preço'].get().strip())
                
                if self.salvar_dados():
                    self.atualizar_listagem()
                    self.atualizar_estatisticas()
                    messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao salvar dados")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")
        
        ctk.CTkButton(
            janela,
            text="💾 Salvar Alterações",
            command=atualizar,
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color="#5cb85c"
        ).pack(pady=20)
    
    def remover_livro_selecionado(self):
        """Remove livro selecionado"""
        if not hasattr(self, 'tree') or not self.tree.winfo_exists():
            messagebox.showwarning("Atenção", "Lista não disponível")
            return
            
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um livro para remover")
            return
        
        item = self.tree.item(selecionado[0])
        livro_id, titulo = item['values'][0], item['values'][1]
        
        resposta = messagebox.askyesno(
            "Confirmar Remoção",
            f"Tem certeza que deseja remover o livro '{titulo}'?"
        )
        
        if resposta:
            self.livros = [l for l in self.livros if l['id'] != livro_id]
            if self.salvar_dados():
                self.atualizar_listagem()
                self.atualizar_estatisticas()
                messagebox.showinfo("Sucesso", "Livro removido com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao salvar dados")
    
    def emprestar_livro(self):
        """Realiza empréstimo de livro"""
        if not hasattr(self, 'tree_emprestimos') or not self.tree_emprestimos.winfo_exists():
            messagebox.showwarning("Atenção", "Lista não disponível")
            return
            
        selecionado = self.tree_emprestimos.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um livro para emprestar")
            return
        
        item = self.tree_emprestimos.item(selecionado[0])
        livro_id, titulo, status = item['values'][0], item['values'][1], item['values'][3]
        
        if "Emprestado" in status:
            messagebox.showwarning("Atenção", "Este livro já está emprestado!")
            return
        
        # Diálogo personalizado para entrada do nome
        dialog = ctk.CTkInputDialog(text="Digite o nome da pessoa:", title="Empréstimo de Livro")
        pessoa = dialog.get_input()
        
        if pessoa and pessoa.strip():
            livro = next((l for l in self.livros if l['id'] == livro_id), None)
            if livro:
                livro['disponivel'] = False
                livro['emprestado_para'] = pessoa.strip()
                if self.salvar_dados():
                    self.atualizar_lista_emprestimos()
                    self.atualizar_estatisticas()
                    messagebox.showinfo("Sucesso", f"Livro '{titulo}' emprestado para {pessoa.strip()}!")
                else:
                    messagebox.showerror("Erro", "Erro ao salvar dados")
    
    def devolver_livro(self):
        """Realiza devolução de livro"""
        if not hasattr(self, 'tree_emprestimos') or not self.tree_emprestimos.winfo_exists():
            messagebox.showwarning("Atenção", "Lista não disponível")
            return
            
        selecionado = self.tree_emprestimos.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um livro para devolver")
            return
        
        item = self.tree_emprestimos.item(selecionado[0])
        livro_id, titulo, status = item['values'][0], item['values'][1], item['values'][3]
        
        if "Disponível" in status:
            messagebox.showwarning("Atenção", "Este livro já está disponível!")
            return
        
        livro = next((l for l in self.livros if l['id'] == livro_id), None)
        if livro:
            pessoa = livro['emprestado_para']
            livro['disponivel'] = True
            livro['emprestado_para'] = ""
            if self.salvar_dados():
                self.atualizar_lista_emprestimos()
                self.atualizar_estatisticas()
                messagebox.showinfo("Sucesso", f"Livro '{titulo}' devolvido por {pessoa}!")
            else:
                messagebox.showerror("Erro", "Erro ao salvar dados")
    
    def atualizar_lista_emprestimos(self):
        """Atualiza a lista de empréstimos"""
        if not hasattr(self, 'tree_emprestimos') or not self.tree_emprestimos.winfo_exists():
            return
            
        for item in self.tree_emprestimos.get_children():
            self.tree_emprestimos.delete(item)
        
        for livro in sorted(self.livros, key=lambda x: x['titulo']):
            status = "✅ Disponível" if livro['disponivel'] else "❌ Emprestado"
            emprestado_para = livro['emprestado_para'] if not livro['disponivel'] else "-"
            self.tree_emprestimos.insert("", "end", values=(
                livro['id'],
                livro['titulo'],
                livro['autor'],
                status,
                emprestado_para
            ))
    
    def calcular_estatisticas(self):
        """Calcula estatísticas da biblioteca"""
        total = len(self.livros)
        disponiveis = len([l for l in self.livros if l['disponivel']])
        emprestados = total - disponiveis
        
        precos = [l['preco'] for l in self.livros if l['preco'] > 0]
        preco_medio = sum(precos) / len(precos) if precos else 0
        
        anos = [l['ano'] for l in self.livros] if self.livros else [0]
        
        return {
            'total': total,
            'disponiveis': disponiveis,
            'emprestados': emprestados,
            'preco_medio': preco_medio,
            'ano_recente': max(anos) if anos else 0,
            'ano_antigo': min(anos) if anos else 0
        }
    
    def atualizar_estatisticas(self):
        """Atualiza os cards de estatísticas"""
        stats = self.calcular_estatisticas()
        
        if hasattr(self, 'stats_labels'):
            for label in self.stats_labels.values():
                if label.winfo_exists():
                    pass
            
            if 'total_livros' in self.stats_labels and self.stats_labels['total_livros'].winfo_exists():
                self.stats_labels['total_livros'].configure(text=str(stats['total']))
            if 'disponiveis' in self.stats_labels and self.stats_labels['disponiveis'].winfo_exists():
                self.stats_labels['disponiveis'].configure(text=str(stats['disponiveis']))
            if 'emprestados' in self.stats_labels and self.stats_labels['emprestados'].winfo_exists():
                self.stats_labels['emprestados'].configure(text=str(stats['emprestados']))
            if 'preco_medio' in self.stats_labels and self.stats_labels['preco_medio'].winfo_exists():
                self.stats_labels['preco_medio'].configure(text=f"R$ {stats['preco_medio']:.2f}")
    
    def filtrar_lista(self, filtro):
        """Filtra a lista de livros"""
        self.atualizar_listagem(filtro)
    
    def limpar_formulario(self):
        """Limpa o formulário de cadastro"""
        for entry in self.entries.values():
            if entry.winfo_exists():
                entry.delete(0, 'end')
    
    def limpar_conteudo(self):
        """Limpa o conteúdo da área principal"""
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()
    
    def sair(self):
        """Fecha o aplicativo"""
        self.salvar_dados()
        self.root.quit()
        self.root.destroy()
    
    def executar(self):
        """Executa a aplicação"""
        self.root.mainloop()

# Executar a aplicação
if __name__ == "__main__":
    try:
        app = SistemaBiblioteca()
        app.executar()
    except Exception as e:
        print(f"Erro ao executar aplicação: {e}")
        messagebox.showerror("Erro", f"Erro ao iniciar aplicação: {e}")