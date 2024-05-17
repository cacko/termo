from threading import Thread

class StoppableThread(Thread):
    
    def stop(self):
        self._stop()