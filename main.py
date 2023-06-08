import re

def processarArquivo(arquivo, novoArquivo):
  ehBlocoComentario = False
  dicDefines = {}
  achouDefine = False
  for linha in arquivo:
    novaLinha = linha
    novaLinha, ehBlocoComentario = removerComentarios(linha, ehBlocoComentario)
    novaLinha = removerEspaços(novaLinha)
    if ("#" in linha):
      if ("#include" in linha):
        novaLinha = ""
        expandirInclude(linha, novoArquivo)
      if ("#define" in linha):
        linhaDividida = linha.split()
        if len(linhaDividida) == 3:
          chave, valor = linhaDividida[1], linhaDividida[2]
          dicDefines[chave] = valor
          achouDefine = True
          novaLinha = ""
    else:
      if achouDefine:
        novaLinha = trocarValor(novaLinha, dicDefines)
    novoArquivo.write(novaLinha)


def expandirInclude(linha, novoArquivo):
  nomeBiblioteca = ""
  nomeStartIndex = linha.find("<")
  if (nomeStartIndex != -1):
    nomeBiblioteca = linha[nomeStartIndex + 1:len(linha.strip()) - 1]
  nomeStartIndex = linha.find("\"")
  if (nomeStartIndex != -1):
    nomeBiblioteca = linha[nomeStartIndex + 1:len(linha.strip()) - 1]

    arquivoBiblioteca = open(nomeBiblioteca, "r")
    processarArquivo(arquivoBiblioteca, novoArquivo)

def emString(linha, palavra):
  startIndex = linha.find('"')
  endIndex = linha.find('"', startIndex + 1)
  wordIndex = linha.find(palavra)

  if startIndex < wordIndex < endIndex:
    return True
  else:
    return False

def trocarValor(linha, dic):
  novaLinha = linha
  for elemento in dic:
    wordIndex = linha.find(elemento)
    if wordIndex != -1:
      ehString = emString(linha, elemento)
      if not ehString:
        novaLinha = novaLinha.replace(elemento, dic[elemento])

  return novaLinha.strip()


def removerComentarios(linha, ehBlocoComentario):
  if ("/*" in linha):
    return '', True
  if ("*/" in linha):
    return '', False
  if (ehBlocoComentario):
    return '', True
  if ("//" in linha):
    return '', False
  return linha, False


def removerEspaços(linha):
  operadores = r'(\+|\-|\=|\<\=|\>\=|\*|\%|\<|\>|\/)'
  linha = re.sub(r'\s*(' + operadores + r')\s*', r'\1', linha)
  linha = re.sub(r'\s*=\s*', '=', linha)
  linha = re.sub(r'\s*(\(|\{)\s*', r'\1', linha)
  linha = re.sub(r'\s*(\)|\})\s*', r'\1', linha)
  linha = linha.replace('\n', '')
  linha = re.sub("^\s+", '', linha)
  linha = re.sub(r'\s*,\s*', ',', linha)
  linha = re.sub(r'\s*;\s*', ';', linha)
  return linha


nomeArquivo = input("Digite o nome do arquivo: ")
arquivo = open(nomeArquivo, "r")

novoArquivo = open("{}_pre_compiled.c".format(nomeArquivo.removesuffix(".c")), "w")

processarArquivo(arquivo, novoArquivo)
novoArquivo.close()
