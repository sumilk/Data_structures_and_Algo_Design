
class ProductPhotoshoot:
    def __init__(self, product_names, staging_time, photo_time):
        self.product_names = product_names
        self.staging_time = staging_time
        self.photo_time = photo_time

    def optimize_time(self):
        product_list = []
        for i in range(len(self.product_names)):
            product_list.append((int(staging_time[i]), int(photo_time[i]), product_names[i]))

        product_list = sorted(product_list, key=lambda x: (x[0], x[1]))

        product_sequence = [x[2] for x in product_list]
        #print(product_sequence)
        total_staging_time, total_photo_time, total_idle_time = 0,0,0

        for item in product_list:
            total_staging_time += item[0]
            if total_staging_time > total_photo_time:
                total_idle_time += total_staging_time - total_photo_time
                total_photo_time += total_staging_time - total_photo_time
            total_photo_time += item[1]

        return product_sequence, total_photo_time, total_idle_time

if __name__ == '__main__':
    with open('inputPS7.txt','r') as input_file:

        product_names = list(map(lambda x:x.strip(), input_file.readline().split(':')[1].strip().split('/')))
        staging_time = list(map(lambda x:x.strip(), input_file.readline().split(':')[1].strip().split('/')))
        photo_time = list(map(lambda x:x.strip(), input_file.readline().split(':')[1].strip().split('/')))

        product_sequence, total_photo_time, total_idle_time = ProductPhotoshoot(product_names, staging_time, photo_time).optimize_time()

    with open('outputPS7.txt', 'w') as output_file:
        product_sequence = ','.join(product_sequence)
        output_file.write(f'Product Sequence: {product_sequence}\n')
        output_file.write(f'Total time to complete photoshoot: {total_photo_time} minutes\n')
        output_file.write(f'Idle time for Xavier: {total_idle_time} minutes')
