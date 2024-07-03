from controller import MatrixController
from pingpongeffect import PingPongEffect


if __name__ == "__main__":
	controller = MatrixController()
	controller.add_to_layers(PingPongEffect)
	controller.add_to_layers(PingPongEffect)
	controller.run()
