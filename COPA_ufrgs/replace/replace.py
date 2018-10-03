import sys

nome = sys.argv[1]
params = sys.argv[2]

if params == '':
    print('Parametros nao encontrados')
    exit(-1)

arq = open(nome, 'r')
todo_conteudo = arq.read()
arq.close()
ax = params.split('@')
ciq = 1
varis = {}
print(ax)
while ciq < len(ax):
    avar = ax[ciq].split("=")
    var = avar[0]
    val = avar[1]
    print("var: " + var + " = " + val)
    todo_conteudo = todo_conteudo.replace(str('$' + var), val)
    ciq += 1

arq = open(nome, 'w')
arq.write(todo_conteudo)
arq.close()
