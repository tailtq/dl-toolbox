import glob


if __name__ == '__main__':
    summary_paths = ['training_set', 'val_set', 'test_set']

    for path in summary_paths:
        files = glob.glob('{}/*.JPG'.format(path))
        summary_file = '{}/summary.txt'.format(path)

        with open(summary_file, 'w+') as s:
            s.write('\n'.join(files))
            s.close()
