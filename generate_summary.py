import glob

def generate_summary(directories):
    for directory in directories:
        txt_files = glob.glob(directory + '/*.jpg')

        f = open(directory + '/summary.txt', 'w+')
        f.write('\n'.join(txt_files))
        f.close()


if __name__ == '__main__':
    generate_summary(['training_set', 'val_set'])
