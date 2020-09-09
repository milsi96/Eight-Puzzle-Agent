class Logger:
    def create(self, name):
        return open(name, "a")

    def open(self, name):
        return open(name, "r")

    def append(self, file, line):
        file.write(line + "\n")

    def close(self, file):
        file.close()
