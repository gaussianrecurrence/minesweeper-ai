from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input,
    Conv2D,
    Dropout
)


class MinesweeperConvNet(Model):
    __CLASSES = 10
    __METRICS = ["accuracy"]
    __ACTIVATION = "sigmoid"
    __LAYERS_PARAMETERS = (
        (__CLASSES, 5, 0.5),
        (8, 5, 0.5),
        (6, 7, 0.3),
        (4, 7, 0.3),
        (2, 9, 0.1),
        (1, 9, None),
    )
    __LOSS_FUNCTION = "binary_crossentropy"

    def __init__(self, rows: int, columns: int):
        """
        Class constructor

        :param rows: Number of rows of the grid
        :param columns: Number of columns of the grid
        """

        x = Input(shape=(rows, columns, self.__CLASSES), name="input")

        f = x
        for i, (depth, filter_size, drop_prob) in enumerate(self.__LAYERS_PARAMETERS):
            f = Conv2D(depth, (filter_size, filter_size), padding="same", name="conv_{}_{}_{}".format(
                i, depth, filter_size), activation=self.__ACTIVATION)(f)

            if drop_prob is not None:
                f = Dropout(drop_prob, name="dropout_{}_{}".format(i, drop_prob))(f)

        Model.__init__(self, inputs=x, outputs=f)

    def compile(self, optimizer: str, **kwargs):

        Model.compile(self, optimizer, loss=self.__LOSS_FUNCTION,
                      metrics=self.__METRICS, **kwargs)
