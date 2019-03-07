import rpyc
from rpyc.utils.server import ThreadedServer


class CalculatorService(rpyc.Service):
    def exposed_add(self, a, b):
        return a + b
    def exposed_sub(self, a, b):
        return a - b
    def exposed_mul(self, a, b):
        return a * b
    def exposed_div(self, a, b):
        return a / b
    def exposed_func(self, a, b):
        return self.exposed_add(a, b)

t  = ThreadedServer(CalculatorService(), port=1233)
t.start()