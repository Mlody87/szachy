class A:
    def __init__(self,nr):
        self._nr = nr


lista = []

a = A(1)
b = A(1)
c = A(1)
d = A(1)
e = A(1)
f = A(1)

podlistaA = [a,b,c]
podlistaB = [d,e]
podlistaC = [f,]

lista.append(podlistaA)
lista.append(podlistaB)
lista.append(podlistaC)

for x in lista:
    print("Rozmiar: ",len(x))