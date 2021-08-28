from .main import evaluate

def generate_caption(image: bytes):
  result, _ = evaluate(image)
  return ' '.join(result)
