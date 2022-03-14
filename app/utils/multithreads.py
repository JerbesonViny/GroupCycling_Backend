from threading import Thread

class Th(Thread):
  
  def __init__(self, num: int, func) -> None:
    Thread.__init__(self)
    self.num = num
    self.function = func

  def run(self) -> None:
    self.function()
