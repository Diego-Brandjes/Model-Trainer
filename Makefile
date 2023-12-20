# Made by	 : Diego Brandjes 
# Date		 : 20-12-2023 

# Makefile for image annotation and creating positive samples

# - positive : 	to create and annotate positive images.
# - negative : 	to create and annotate negative images.
# - vec		 : 	to create the vec file.
# - train	 : 	to train the model.
# - clean	 : 	removes all model data, used for retraining model.

# - detect	 : 	run to detect faces in images.
# - reset	 : 	clears the input files for detection.

# Set paths and variables
NEGATIVE_IMAGES_FOLDER 		= no_faces
POSITIVE_IMAGES_FOLDER		= faces
XML_FOLDER					= xml
NEGATIVE_ANNOTATION_FILE 	= negative.txt
POSITIVE_ANNOTATION_FILE 	= positive.txt
POSITIVE_VECTOR_FILE 		= model.vec

POSITIVE_AMOUNT				= 100
NEGATIVE_AMOUNT				= 120

# Positive
positive:
	python scripts/capture.py $(POSITIVE_IMAGES_FOLDER) $(POSITIVE_AMOUNT)			
	opencv_annotation \
		--maxWindowHeight=1000 \
		--resizeFactor=3 \
		--annotations=$(POSITIVE_ANNOTATION_FILE) \
		--images=$(POSITIVE_IMAGES_FOLDER)

# Negative
negative:
	python scripts/capture.py $(NEGATIVE_IMAGES_FOLDER) $(NEGATIVE_AMOUNT)
	python scripts/createNegative.py $(NEGATIVE_IMAGES_FOLDER) $(NEGATIVE_ANNOTATION_FILE)


# Vec
vec:
	opencv_createsamples \
		-info $(POSITIVE_ANNOTATION_FILE) \
		-bg $(NEGATIVE_ANNOTATION_FILE) \
		-vec $(POSITIVE_VECTOR_FILE) \
		-w 30 \
		-h 30

train:
	opencv_traincascade \
		-data $(XML_FOLDER) \
		-vec $(POSITIVE_VECTOR_FILE) \
		-bg $(NEGATIVE_ANNOTATION_FILE) \
		-precalcValBufSize 3000 \
		-precalcIdxBufSize 3000 \
		-numPos $(POSITIVE_AMOUNT) \
		-numNeg $(NEGATIVE_AMOUNT) \
		-w 30 \
		-h 30 \
		-numStages 25

# Clear files
clean-a:
	make clean
	- rm -f $(POSITIVE_IMAGES_FOLDER)/*.png
	- rm -f $(NEGATIVE_IMAGES_FOLDER)/*.png
	- rm -f $(filter-out $(XML_FOLDER)/cascade.xml, $(wildcard $(XML_FOLDER)/*.xml))
	- rm -f $(POSITIVE_ANNOTATION_FILE)
	- rm -f $(NEGATIVE_ANNOTATION_FILE)
	- rm -f $(POSITIVE_VECTOR_FILE)

detect:
	python3 scripts/check.py

webcam:
	python3 scripts/webcam.py

# Reset
clean:
	- rm -f output/*.png
	- rm -f input/*.png
	- rm -f output/*.jpg
	- rm -f input/*.jpg

# Fully train the model from scratch
train-f:
	make clean
	make negative
	@echo Negatives done, starting positives in 2 seconds...
	make positive
	make vec
	@echo VEC is finished!
	@echo starting model training in 3 seconds...
	make train
	@echo Model is trained!