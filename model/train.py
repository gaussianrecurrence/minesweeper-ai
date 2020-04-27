import numpy as np
from tensorflow.keras.callbacks import (
    TensorBoard,
    ModelCheckpoint
)

from model.cnn import MinesweeperConvNet
from dataset.generator import DatasetGenerator


class Trainer(object):
    __BATCH_SIZE = 64
    __OPTIMIZER = "adam"
    __LOG_DIR = ".tfboard"
    __SAVE_PATH = ".checkpoints/cp-latest.ckpt"
    __CKPT_PATH = ".checkpoints/cp-{epoch:04d}.ckpt"

    def __init__(self):

        rows, columns = 16, 30
        mines_percentage = .15
        self._model = MinesweeperConvNet(rows, columns)
        self._generator = DatasetGenerator(rows, columns,
                                           mines_percentage, self.__BATCH_SIZE)
        self._tfboard = TensorBoard(
            log_dir=self.__LOG_DIR, histogram_freq=2)
        self._autosaver = ModelCheckpoint(
            filepath=self.__CKPT_PATH,
            verbose=1,
            save_weights_only=True,
            period=4)

        self._model.compile(self.__OPTIMIZER)
        print(self._model.predict(np.zeros((1, 16, 30, 10), np.float32)))

    def __call__(self):
        self._model.fit_generator(self._generator,
                                  shuffle=False,
                                  epochs=1 << 20,
                                  validation_steps=1,
                                  validation_freq=16,
                                  steps_per_epoch=32,
                                  validation_data=self._generator,
                                  callbacks=[self._tfboard, self._autosaver])

    def save_model(self):
        self._model.save_weights(self.__SAVE_PATH)


if __name__ == "__main__":

    trainer = Trainer()

    try:
        trainer()
        exit(0)
    except KeyboardInterrupt:
        print("[WARN] Ctrl+C pressed. Shutting down...")
        trainer.save_model()
        exit(130)
