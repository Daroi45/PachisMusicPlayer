from presenter.presenter import Presenter
from tkinterdnd2 import DND_FILES, TkinterDnD

if __name__ == "__main__":
	root = TkinterDnD.Tk()
	app = Presenter(root)
	root.mainloop()
