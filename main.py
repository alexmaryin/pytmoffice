from data.repository.db import DataBaseConnection, connection_str
from data.repository.intel_repo import IntelRepository


def main():
    db = DataBaseConnection(connection_str)
    repo = IntelRepository(db)
    groups = repo.get_groups()
    print("*********************")
    for group in groups:
        print(group.ID, group.group_name)
    print("*********************")

    groups_baikal = repo.get_groups('слав')
    print("*********************")
    for group in groups_baikal:
        print(f'{group.ID}\t\t{group.group_name}')
    print("*********************")


    # result = db.session.query(License).all()
    # for ld in result:
    #     print(f'{ld.id}\t{ld.licensor.name}\t{ld.licensee.name}')
    #     for ass in ld.objects:
    #         print(f'\t\t- {ass.object.number}\t{ass.object.name}')
    #     # plt.figure()
    #     # plt.imshow(Image.open(io.BytesIO(patent.image)))
    #     # plt.show()


if __name__ == '__main__':
    main()
