from .train_model import predict
from typing import List, Tuple, Union, Literal
from .area import AreaCoordinates


class ModelRecognize:

    def find_celebrities(self, path_to_image_file) -> List[Union[Tuple, Tuple[Literal['unknown']]]]:
        return predict(path_to_image_file)

    def get_coordinates(self, celebrity, corner_coordinates) -> AreaCoordinates:
        return AreaCoordinates(celebrity, corner_coordinates)
