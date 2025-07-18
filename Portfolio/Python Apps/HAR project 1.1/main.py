#Accounts test + menu test (Unit test #3 - written by Hasan)
from menu import Menu
from time import sleep

menu = Menu()
exit = False
while not exit:
  menu.displayMenu()
  sleep(1)
  choice = menu.getChoice()
  sleep(2)
  exit = menu.handleChoice(choice)
  sleep(3)
  print("\n")
quit()
