from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from glob import glob
import os
import time
import RPi_I2C_driver as i2c
from picamera import PiCamera
ROOT = os.getcwd() + '/training/'
ROOT_PREDICTION = os.getcwd() + '/prediction/'
app = ClarifaiApp(api_key="77ffb4a76be24b7e980b29ca43227ebb")
lcd = i2c.lcd()
def train():
	app.inputs.delete_all()
	folders = ["superman", "batman"] # Lists out all categories
	for folder in folders:
		not_concepts = folders.copy()
		not_concepts.remove(folder)
		print(ROOT+folder)
		image_set = create_image_set(ROOT+folder+"/", concepts=[folder], not_concepts=not_concepts)
		app.inputs.bulk_create_images(image_set)
	model = app.models.get('sbman')
	model.train()

def predict(url):
	model = app.models.get('sbman')
	return model.predict_by_url(url)

def predict_by_file(fpath):
	model = app.models.get('sbman')
	return model.predict_by_filename(fpath)


def create_image_set(path, concepts, not_concepts):
	images = []
	for file in glob(os.path.join(path, '*.jpg')):
		print(file)
		i = ClImage(filename=file, concepts=concepts, not_concepts=not_concepts)
		images.append(i)
	return images

if __name__ == "__main__":
	i = 0
	if input("Train? ")[0].lower() == 'y':
		train()
	camera = PiCamera()
	while True:
		imgs = glob(os.path.join(ROOT_PREDICTION, '*.jpg'))
		print(imgs)
		if len(imgs) == 0:
			camera.resolution = (100, 100)
			camera.capture('prediction/{}.jpg'.format(i))
		else:
			print("Om nom nom")
			results = predict_by_file(imgs[0])['outputs'][0]['data']['concepts']
			i_r = lambda x: '{}: {}'.format(x['id'], x['value'])
			print(list(map(i_r, results)))
			os.remove(imgs[0])
			lcd.lcd_display_string(''.join(list(map(i_r, results))), 1)
		time.sleep(5.0)
		i += 1
