# Função que verifica se existe um argumento específico em uma lista
def search_arg(list_args: list, key: str) -> int:
  try:
    position = list_args.index(key)
  except:
    position = None

  return position