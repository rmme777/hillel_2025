import time

class FunctionLife:

    def __enter__(self):
        self.start = time.monotonic()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
            self.end = time.monotonic() - self.start
            if self.end > 3:
                raise Exception("Функция проработала больше 3 секунд")

def test_function(time_sleep):
    for i in range(5):
        print(i)
        time.sleep(time_sleep)

with FunctionLife():
    test_function(1)

