__author__ = 'kakit'

class PiCamera():
    def __init__(self):
        pass

    def capture(self, output, format=None, use_video_port=False, resize=None, splitter_port=0, **options):
        pass

    def close(self):
        pass

    def start_recording(self, output, format=None, resize=None, splitter_port=1, **options):
        pass

    def stop_recording(self, splitter_port=1):
        pass
