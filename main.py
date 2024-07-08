from controller import MatrixController
from fontcycler import FontCycler


if __name__ == "__main__":
	controller = MatrixController()
	controller.add_to_layers(FontCycler)
	controller.run()
