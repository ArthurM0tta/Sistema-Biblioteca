def alugar_livro(self):
    alugar_janela = tk.Toplevel(self.root)
    alugar_janela.title("Aluguel de Livro")

    self.titulo_label = tk.Label(alugar_janela, text="Título do Livro:")
    self.titulo_label.pack()

    self.titulo_var = tk.StringVar()
    self.titulo_entry = tk.Entry(alugar_janela, textvariable=self.titulo_var)
    self.titulo_entry.pack()

    self.autor_label = tk.Label(alugar_janela, text="Autor do Livro:")
    self.autor_label.pack()

    self.autor_var = tk.StringVar()
    self.autor_entry = tk.Entry(alugar_janela, textvariable=self.autor_var)
    self.autor_entry.pack()

    def confirmar_aluguel():
        titulo = self.titulo_var.get()
        autor = self.autor_var.get()

        # Verificar se o livro está disponível
        consulta_disponibilidade = "SELECT * FROM livros WHERE titulo = ? AND autor = ? AND disponivel = 1"
        dados_para_consulta = (titulo, autor)
        self.cursor.execute(consulta_disponibilidade, dados_para_consulta)
        livro_disponivel = self.cursor.fetchone()

        if livro_disponivel:
            # Atualizar a disponibilidade do livro para não disponível (0)
            id_livro = livro_disponivel[0]
            self.cursor.execute("UPDATE livros SET disponivel = 0 WHERE id = ?", (id_livro,))
            self.conn.commit()

            # Registrar o aluguel na tabela de aluguéis (exemplo simplificado)
            data_aluguel = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute("INSERT INTO alugueis (id_livro, data_aluguel) VALUES (?, ?)", (id_livro, data_aluguel))
            self.conn.commit()

            messagebox.showinfo('Livro Alugado', 'Livro alugado com sucesso!')
        else:
            messagebox.showinfo('Livro Indisponível', 'O livro não está disponível para aluguel.')

        alugar_janela.destroy()

    # Botão de confirmação
    self.confirmar_aluguel_button = tk.Button(alugar_janela, text="Confirmar Aluguel", command=confirmar_aluguel)
    self.confirmar_aluguel_button.pack()
