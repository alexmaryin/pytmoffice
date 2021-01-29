import io

from PIL import Image
from data.model.base import *
from data.repository.db import DataBaseConnection, connection_str
import matplotlib.pyplot as plt


def main():
    db = DataBaseConnection(connection_str)
    result = db.session.query(License).order_by(License.licensorID).all()
    for ld in result:
        print(f'{ld.id}\t{ld.licensor.name}\t{ld.licensee.name}')
        for ass in ld.objects:
            print(f'\t\t- {ass.object.number}\t{ass.object.name}')
        # plt.figure()
        # plt.imshow(Image.open(io.BytesIO(patent.image)))
        # plt.show()


if __name__ == '__main__':
    main()
