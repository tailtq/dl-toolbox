import random
from compare_two_directories import get_all_images
import time

random.seed(10)
root_directories = ["visualization/data"]
dest_directory = "visualization"
names = ["images"]
should_remove_base = True

if __name__ == "__main__":
    for index, directory in enumerate(root_directories):
        files = get_all_images(directory)
        random.shuffle(files)

        for index1, file in enumerate(files):
            # start = time.time()
            files[index1] = file.replace(dest_directory + "/", "")
            # end = time.time()

            # start1 = time.time()
            # files[index] = "/".join(file.split("/")[1:])
            # end1 = time.time()
            # print("End time: ", (end - start) * 1000, (end1 - start1) * 1000)

        file_name = names[index] if index < len(names) else directory.split("/")[-1]
        file_name = file_name + ".txt"

        f = open(f"{dest_directory}/{file_name}", "w+")
        f.write("\n".join(files))
        f.close()
