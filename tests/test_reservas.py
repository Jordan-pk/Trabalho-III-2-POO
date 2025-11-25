import unittest
from datetime import datetime, timedelta
from modelos import Cliente, Quarto
from servicos import SistemaReservas


class TestReservas(unittest.TestCase):
def setUp(self):
self.sistema = SistemaReservas()
self.q = Quarto(200, 'Single', 100.0)
self.sistema.adicionar_quarto(self.q)
self.c = Cliente(10, 'Teste', '000', 't@t', '000