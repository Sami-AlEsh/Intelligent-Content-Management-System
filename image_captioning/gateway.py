from .main import evaluate

def generate_caption(image: bytes):
  result, _ = evaluate(image)
  print('lllllllllllllll')
  print(result)
  return ' '.join(result)
