from datetime import datetime
from modelos import Reserva, Quarto, Cliente


class SistemaReservas:
def __init__(self):
self.quartos = {}
self.reservas = {}
self.clientes = {}
self._next_reserva_id = 1


def adicionar_quarto(self, quarto: Quarto):
self.quartos[quarto.numero] = quarto


def cadastrar_cliente(self, cliente: Cliente):
self.clientes[cliente.id_cliente] = cliente


def consultar_disponibilidade(self, numero_quarto: int) -> bool:
quarto = self.quartos.get(numero_quarto)
if not quarto:
raise ValueError("Quarto não existe")
return quarto.disponivel


def realizar_reserva(self, id_cliente: int, numero_quarto: int, data_checkin: datetime, data_checkout: datetime, paga_em: Optional[datetime] = None) -> Reserva:
cliente = self.clientes.get(id_cliente)
if not cliente:
raise ValueError("Cliente não cadastrado")
quarto = self.quartos.get(numero_quarto)
if not quarto:
raise ValueError("Quarto não encontrado")
if not quarto.disponivel:
raise ValueError("Quarto indisponível")
reserva = Reserva(self._next_reserva_id, cliente, quarto, data_checkin, data_checkout)
sucesso = reserva.confirmar_reserva(paga_em)
if not sucesso:
raise RuntimeError("Falha ao confirmar reserva")
self.reservas[self._next_reserva_id] = reserva
self._next_reserva_id += 1
return reserva


def cancelar_reserva(self, id_reserva: int, agora: Optional[datetime] = None) -> bool:
reserva = self.reservas.get(id_reserva)
if not reserva:
raise ValueError("Reserva não encontrada")
return reserva.cancelar_reserva(agora)


def emitir_fatura(self, id_reserva: int) -> str:
reserva = self.reservas.get(id_reserva)
if not reserva:
raise ValueError("Reserva não encontrada")
valor = reserva.valor_total or reserva.calcular_total()
conteudo = f"Fatura - Reserva {id_reserva}\nCliente: {reserva._cliente.nome}\nQuarto: {reserva._quarto.numero}\nValor total: R$ {valor:.2f}\n"
# Para simplificar, retorna string. Poderia salvar em arquivo.
return conteudo