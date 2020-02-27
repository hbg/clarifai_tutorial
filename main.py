from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from glob import glob
import os
ROOT = os.getcwd() + '/training/'
ROOT_PREDICTION = os.getcwd() + '/prediction/'
app = ClarifaiApp(api_key="c52037fe09f14d559e2e11857bfba297")

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
	if input("Train? ")[0].lower() == 'y':
		train()
	while True:
		imgs = glob(os.path.join(ROOT_PREDICTION, '*.jpg'))
		if len(imgs) == 0:
		  """
		  """
		else:
		  print("Om nom nom")
		  print(predict_by_file(imgs[0]))
		  os.remove(imgs[0])
