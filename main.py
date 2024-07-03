from controller import MatrixController
from pingpongeffect import PingPongEffect


if __name__ == "__main__":
	controller = MatrixController()
	matrix = controller.matrix
	controller.add_to_queue(PingPongEffect(matrix=matrix))
	controller.run()
