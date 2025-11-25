from datetime import datetime, timedelta
from modelos import Cliente, Funcionario, Quarto
from servicos import SistemaReservas


def demo():
sistema = SistemaReservas()


# criar quartos
q101 = Quarto(101, 'Single', 150.0)
q102 = Quarto(102, 'Double', 250.0)
sistema.adicionar_quarto(q101)
sistema.adicionar_quarto(q102)


# cadastrar cliente e funcionario
c1 = Cliente(1, 'Ana Silva', '12345678900', 'ana@exemplo.com', '1199999')
f1 = Funcionario(1, 'Paulo', '09876543211', 'paulo@hotel.com', 'Recepção')
sistema.cadastrar_cliente(c1)


# consultar disponibilidade
print('Q101 disponível?', sistema.consultar_disponibilidade(101))


# realizar reserva com pagamento agora
checkin = datetime.now() + timedelta(days=1)
checkout = checkin + timedelta(days=3)
reserva = sistema.realizar_reserva(1, 101, checkin, checkout, paga_em=datetime.now())
print('Reserva criada:', reserva.id_reserva, 'Valor:', reserva.valor_total)


# tentar cancelar após 25 horas -> deve falhar
futuro = datetime.now() + timedelta(hours=25)
ok = sistema.cancelar_reserva(reserva.id_reserva, agora=futuro)
print('Cancelamento após 25h:', ok)


# cancelar dentro de 24h (novo cenário)
reserva2 = sistema.realizar_reserva(1, 102, checkin, checkout, paga_em=datetime.now())
ok2 = sistema.cancelar_reserva(reserva2.id_reserva, agora=datetime.now() + timedelta(hours=5))
print('Cancelamento em 5h:', ok2)


# checkout e revisão do quarto
reserva.confirmar_checkout()
f1.revisar_quarto(q101)
print('Quarto 101 revisado?', q101.revisado)


# emitir fatura
print(sistema.emitir_fatura(reserva.id_reserva))


if __name__ == '__main__':
demo()