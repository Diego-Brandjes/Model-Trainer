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

# image filetype used
FILETYPE					= .png

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
		-precalcValBufSize 6000 \
		-precalcIdxBufSize 6000 \
		-numPos $(POSITIVE_AMOUNT) \
		-numNeg $(NEGATIVE_AMOUNT) \
		-w 30 \
		-h 30

# Clear files
clean:
	- rm -f $(POSITIVE_IMAGES_FOLDER)/*$(FILETYPE)
	- rm -f $(NEGATIVE_IMAGES_FOLDER)/*$(FILETYPE)
	- rm -f $(filter-out $(XML_FOLDER)/cascade.xml, $(wildcard $(XML_FOLDER)/*.xml))

	- rm -f $(POSITIVE_ANNOTATION_FILE)
	- rm -f $(NEGATIVE_ANNOTATION_FILE)
	- rm -f $(POSITIVE_VECTOR_FILE)

detect:
	python3 scripts/check.py

# Reset
reset:
	- rm -f output/*$(FILETYPE)
	- rm -f input/*$(FILETYPE)

# Fully train the model from scratch
train-f:
	make clean
	make negative
	@echo Negatives done, starting positives in 2 seconds...
	sleep 2
	make positive
	make vec
	@echo VEC is finished!
	@echo starting model training in 3 seconds...
	sleep 3
	make train
	@echo Model is trained!