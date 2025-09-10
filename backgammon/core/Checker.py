class Checker:
  """
  Clase que representa una ficha del juego Backgammon.
  """
  
  def __init__(self, color):
    """
    Inicializa una ficha con su color.
    
    Args:
      color (str): Color de la ficha ("white" o "black")
    """
    self.color = color
    self.position = None
  
  def __str__(self):
    """Representación en string de la ficha"""
    return f"Checker({self.color})"
  
  def __repr__(self):
    """Representación para debugging"""
    return f"Checker(color='{self.color}', position={self.position})"