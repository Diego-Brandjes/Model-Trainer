# Made by	 : Diego Brandjes 
# Date		 : 21-12-2023 

# Makefile for image annotation and creating positive samples

# - positive : 	to create and annotate positive images.
# - negative : 	to create and annotate negative images.
# - vec		 : 	to create the vec file.
# - train	 : 	to train the model.
# - clean	 : 	removes all model data, used for retraining model.

# - detect	 : 	run to detect faces in images.
# - reset	 : 	clears the input files for detection.

# Set paths and variables
NEGATIVE_IMAGES_FOLDER 		= false
POSITIVE_IMAGES_FOLDER		= true
XML_FOLDER					= xml
NEGATIVE_ANNOTATION_FILE 	= negative.txt
POSITIVE_ANNOTATION_FILE 	= positive.txt
POSITIVE_VECTOR_FILE 		= model.vec
OUTPUT_FOLDER				= output
INPUT_FOLDER				= input

RED := $(shell tput setaf 1)
GREEN := $(shell tput setaf 2)
RESET := $(shell tput sgr0)

load_folders:
	- rm -rf $(POSITIVE_IMAGES_FOLDER) $(NEGATIVE_IMAGES_FOLDER)
	mkdir $(POSITIVE_IMAGES_FOLDER) $(NEGATIVE_IMAGES_FOLDER)
	python scripts/copy_folders.py $(POSITIVE_IMAGES_FOLDER) $(NEGATIVE_IMAGES_FOLDER)

# Positive
annotate:
	python scripts/create_negatives.py $(NEGATIVE_IMAGES_FOLDER) $(NEGATIVE_ANNOTATION_FILE)
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
		-w 30 \
		-h 30
		@echo "$(GREEN)VEC CREATED$(RESET)"
		@echo "$(RED)Confirm positive count$(RESET)"
		python scripts/confirm_positives.py

#POSITIVE_AMOUNT := $(shell type positive_amount.tmp) #use on windows devices
#NEGATIVE_AMOUNT := $(shell type negative_amount.tmp)

POSITIVE_AMOUNT := $(shell cat positive_amount.tmp) # use on UNIX
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
		-w 30 \
		-h 30 \
		-numStages 20

# Clear files
clean:

	- rm -f $(filter-out $(XML_FOLDER)/cascade.xml, $(wildcard $(XML_FOLDER)/*.xml))
	- rm -f $(POSITIVE_ANNOTATION_FILE)
	- rm -f $(NEGATIVE_ANNOTATION_FILE)
	- rm -f $(POSITIVE_VECTOR_FILE)
	- rm -rf $(POSITIVE_IMAGES_FOLDER) $(NEGATIVE_IMAGES_FOLDER)
	- rm -f negative_amount.tmp positive_amount.tmp

detect:

	python3 scripts/check_images.py $(INPUT_FOLDER) $(OUTPUT_FOLDER)
	- rm -f $(OUTPUT_FOLDER)/*

webcam:
	python3 scripts/webcam.py
	
# Fully train the model from scratch
train: clean load_folders annotate vec

	- mkdir -p $(INPUT_FOLDER) $(OUTPUT_FOLDER)	
	@echo "POSITIVE_AMOUNT: $$(cat positive_amount.tmp)"
	@echo "NEGATIVE_AMOUNT: $$(cat negative_amount.tmp)"
	make train-s
	make clean
	@echo "$(GREEN)Model is trained! XML is ready for use$(RESET)"