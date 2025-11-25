# Sistema de Reservas - Projeto em Python

Este repositório contém uma implementação modular em Python do modelo UML fornecido para um sistema de reservas (hotel). Está dividido em arquivos conforme responsabilidades: `modelos.py`, `servicos.py`, `main.py`, `tests/test_reservas.py` e `README.md`.


## arquivos

### modelos.py
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional

class Pessoa(ABC):
    def __init__(self, nome: str, documento: str, email: str):
        self._nome = nome
        self._documento = documento
        self._email = email

    @property
    def nome(self):
        return self._nome

    @property
    def documento(self):
        return self._documento

    @property
    def email(self):
        return self._email

    @abstractmethod
    def exibir_dados(self) -> str:
        pass

class Cliente(Pessoa):
    def __init__(self, id_cliente: int, nome: str, documento: str, email: str, telefone: str):
        super().__init__(nome, documento, email)
        self._id_cliente = id_cliente
        self._telefone = telefone
        self._reservas = []  # associação: 1 cliente pode ter várias reservas

    @property
    def id_cliente(self):
        return self._id_cliente

    @property
    def telefone(self):
        return self._telefone

    def exibir_dados(self) -> str:
        return f"Cliente {self._id_cliente}: {self._nome} - {self._telefone}"

    def solicitar_reserva(self, reserva):
        self._reservas.append(reserva)

class Funcionario(Pessoa):
    def __init__(self, id_funcionario: int, nome: str, documento: str, email: str, cargo: str):
        super().__init__(nome, documento, email)
        self._id_funcionario = id_funcionario
        self._cargo = cargo

    @property
    def id_funcionario(self):
        return self._id_funcionario

    @property
    def cargo(self):
        return self._cargo

    def exibir_dados(self) -> str:
        return f"Funcionario {self._id_funcionario}: {self._nome} - {self._cargo}"

    def revisar_quarto(self, quarto) -> bool:
        # Exemplo simples de revisão: certifica-se que quarto está limpo e disponível
        # Pode ser expandido conforme regras reais
        print(f"Funcionario {self._nome} revisando quarto {quarto.numero}")
        quarto.revisado = True
        return True

class Quarto:
    def __init__(self, numero: int, tipo: str, preco_diaria: float):
        self._numero = numero
        self._tipo = tipo
        self._preco_diaria = preco_diaria
        self._disponivel = True
        self._revisado = False
        self._reservas = []  # agregação: quarto pode ter muitas reservas (histórico)

    @property
    def numero(self):
        return self._numero

    @property
    def tipo(self):
        return self._tipo

    @property
    def preco_diaria(self):
        return self._preco_diaria

    @property
    def disponivel(self):
        return self._disponivel

    @disponivel.setter
    def disponivel(self, value: bool):
        self._disponivel = bool(value)

    @property
    def revisado(self):
        return self._revisado

    @revisado.setter
    def revisado(self, value: bool):
        self._revisado = bool(value)

    def marcar_ocupado(self):
        self._disponivel = False

    def liberar_quarto(self):
        self._disponivel = True

    def adicionar_reserva(self, reserva):
        self._reservas.append(reserva)

class Reserva:
    def __init__(self, id_reserva: int, cliente: Cliente, quarto: Quarto, data_checkin: datetime, data_checkout: datetime):
        self._id_reserva = id_reserva
        self._cliente = cliente
        self._quarto = quarto
        self._data_checkin = data_checkin
        self._data_checkout = data_checkout
        self._valor_total = 0.0
        self._confirmada = False
        self._paga_em: Optional[datetime] = None
        self._cancelada = False

    @property
    def id_reserva(self):
        return self._id_reserva

    @property
    def data_checkin(self):
        return self._data_checkin

    @property
    def data_checkout(self):
        return self._data_checkout

    @property
    def valor_total(self):
        return self._valor_total

    def calcular_total(self) -> float:
        dias = (self._data_checkout - self._data_checkin).days
        if dias <= 0:
            dias = 1
        self._valor_total = dias * self._quarto.preco_diaria
        return self._valor_total

    def confirmar_reserva(self, paga_em: Optional[datetime] = None) -> bool:
        if not self._quarto.disponivel:
            return False
        self.calcular_total()
        self._confirmada = True
        if paga_em:
            self._paga_em = paga_em
        # marca quarto como ocupado
        self._quarto.marcar_ocupado()
        self._quarto.adicionar_reserva(self)
        # associação: cliente solicita reserva
        self._cliente.solicitar_reserva(self)
        return True

    def cancelar_reserva(self, agora: Optional[datetime] = None) -> bool:
        # Regra: só pode ser cancelada até 24h após pagamento (ou seja, dentro de 24h após pago)
        if not self._confirmada:
            print("Reserva não confirmada; nada a cancelar")
            return False
        if self._cancelada:
            return False
        if self._paga_em is None:
            # se não houve pagamento registrado, permitimos cancelamento (negócio pode variar)
            self._cancelada = True
            self._quarto.liberar_quarto()
            return True
        agora = agora or datetime.now()
        delta = agora - self._paga_em
        if delta <= timedelta(hours=24):
            self._cancelada = True
            self._quarto.liberar_quarto()
            return True
        else:
            print("Cancelamento não permitido: passou de 24h após pagamento")
            return False

    def confirmar_checkin(self):
        # placeholder para checkin
        print(f"Check-in confirmado para reserva {self._id_reserva}")

    def confirmar_checkout(self):
        # ao checkout, quarto deve ser revisado por um funcionário
        print(f"Check-out confirmado para reserva {self._id_reserva}")