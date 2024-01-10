# Made by	 : Diego Brandjes 
# Date		 : 10-01-2024 

# Makefile for image annotation and creating a trained model

# ___UNIX VERSION___

# - load_folders : 	to create and load (new)folders. Will also rename and resize all files in the folders prior to copying.
# - annotate 	 : 	to create and annotate images.
# - vec		 	 : 	to create the vec file.
# - train	 	 : 	to train the model.
# - train-s	 	 : 	to only retrain the model on new vec.
# - clean	 	 : 	removes all model data, used for training model.

# - detect	 	 : 	run to detect faces in images.
# - webcam	 	 : 	run to detect faces in webcam video.

# Set paths and variables
NEGATIVE_IMAGES_FOLDER 		= false_faces
POSITIVE_IMAGES_FOLDER		= true_faces
XML_FOLDER					= xml
NEGATIVE_ANNOTATION_FILE 	= negative.txt
POSITIVE_ANNOTATION_FILE 	= positive.txt
POSITIVE_VECTOR_FILE 		= model.vec
OUTPUT_FOLDER				= output
INPUT_FOLDER				= input
BOX_SIZE					= 30
IMAGE_SIZE					= 300

RED := $(shell tput setaf 1)
GREEN := $(shell tput setaf 2)
RESET := $(shell tput sgr0)

load_folders:
	- rm -rf $(POSITIVE_IMAGES_FOLDER) $(NEGATIVE_IMAGES_FOLDER)
	mkdir $(POSITIVE_IMAGES_FOLDER) $(NEGATIVE_IMAGES_FOLDER)
	python3 scripts/handle_folders.py $(POSITIVE_IMAGES_FOLDER) $(NEGATIVE_IMAGES_FOLDER) $(IMAGE_SIZE)

# annotate
annotate:
	python3 scripts/create_negatives.py $(NEGATIVE_IMAGES_FOLDER) $(NEGATIVE_ANNOTATION_FILE)
	opencv_annotation \
		--maxWindowHeight=1000 \
		--resizeFactor=3 \
		--annotations=$(POSITIVE_ANNOTATION_FILE) \
		--images=$(POSITIVE_IMAGES_FOLDER)
	@echo "$(GREEN)DONE ANNOTATING$(RESET)"

# Vec
vec:
	opencv_createsamples \
		-info $(POSITIVE_ANNOTATION_FILE) \
		-bg $(NEGATIVE_ANNOTATION_FILE) \
		-vec $(POSITIVE_VECTOR_FILE) \
		-w $(BOX_SIZE) \
		-h $(BOX_SIZE)
		@echo "$(GREEN)VEC CREATED$(RESET)"
		@echo "$(RED)Confirm positive count$(RESET)"
		python3 scripts/confirm_samples.py

# create the .tmp filed to store sample amounts. Use on UNIX
POSITIVE_AMOUNT := $(shell cat positive_amount.tmp) 
NEGATIVE_AMOUNT := $(shell cat negative_amount.tmp)

train-s:
	opencv_traincascade \
		-data $(XML_FOLDER) \
		-vec $(POSITIVE_VECTOR_FILE) \
		-bg $(NEGATIVE_ANNOTATION_FILE) \
		-precalcValBufSize 3000 \
		-precalcIdxBufSize 3000 \
		-numPos $(POSITIVE_AMOUNT) \
		-numNeg $(NEGATIVE_AMOUNT) \
		-w $(BOX_SIZE) \
		-h $(BOX_SIZE) \
		-numStages 30

# Clear files
clean:
	- rm -f $(filter-out $(XML_FOLDER)/cascade.xml, $(wildcard $(XML_FOLDER)/*.xml))
	- rm -f $(POSITIVE_ANNOTATION_FILE)
	- rm -f $(NEGATIVE_ANNOTATION_FILE)
	- rm -f $(POSITIVE_VECTOR_FILE)
	- rm -f negative_amount.tmp positive_amount.tmp

	- rm -rf $(INPUT_FOLDER) $(OUTPUT_FOLDER)
	- rm -rf $(POSITIVE_IMAGES_FOLDER) $(NEGATIVE_IMAGES_FOLDER)

detect:
	- mkdir -p $(OUTPUT_FOLDER)	
	python3 scripts/check_images.py $(INPUT_FOLDER) $(OUTPUT_FOLDER)
	@echo "$(GREEN)Use 'make reset' to reset the input and output folders.$(RESET)"

reset:
	- rm -f $(INPUT_FOLDER)/* $(OUTPUT_FOLDER)/*

webcam:
	python3 scripts/webcam.py
	
# Fully train the model from scratch
train: clean load_folders annotate vec

	@echo "POSITIVE_AMOUNT: $$(cat positive_amount.tmp)"
	@echo "NEGATIVE_AMOUNT: $$(cat negative_amount.tmp)"
	make train-s
	make clean
	@echo "$(GREEN)Model is trained! XML is ready for use$(RESET)"
	- mkdir -p $(INPUT_FOLDER)	

