import yaml


def change_token(token, file_path):
    with open(file_path) as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)

    doc['TokensVault']['BOT_TOKEN']['token'] = token

    with open(file_path, 'w') as f:
        yaml.dump(doc, f)


if __name__ == '__main__':
    import sys

    change_token(sys.argv[1], sys.argv[2])
