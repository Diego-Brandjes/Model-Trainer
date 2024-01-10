# Made by	 : Diego Brandjes 
# Date		 : 21-12-2023 

# Makefile for image annotation and creating a trained model

# - load_folders : 	to create and load (new)folders. Will also rename all files in the folders prior to copying.
# - annotate 	 : 	to create and annotate images.
# - vec		 	 : 	to create the vec file.
# - train	 	 : 	to train the model.
# - train-s	 	 : 	to only retrain the model on new vec.
# - clean	 	 : 	removes all model data, used for training model.

# - detect	 	 : 	run to detect faces in images.
# - webcam	 	 : 	run to detect faces in webcam video.

#   ____WINDOWS VERSION____

# Set paths and variables
NEGATIVE_IMAGES_FOLDER 		= false
POSITIVE_IMAGES_FOLDER		= true
XML_FOLDER					= xml
NEGATIVE_ANNOTATION_FILE 	= negative.txt
POSITIVE_ANNOTATION_FILE 	= positive.txt
POSITIVE_VECTOR_FILE 		= model.vec
OUTPUT_FOLDER				= output
INPUT_FOLDER				= input
BOX_SIZE					= 30


load_folders:
	-@rmdir /S /Q $(POSITIVE_IMAGES_FOLDER%)
	-@rmdir /S /Q $(NEGATIVE_IMAGES_FOLDER%)
	@if not exist $(POSITIVE_IMAGES_FOLDER) mkdir $(POSITIVE_IMAGES_FOLDER)
	@if not exist $(NEGATIVE_IMAGES_FOLDER) mkdir $(NEGATIVE_IMAGES_FOLDER)
	python3 scripts/copy_folders.py $(POSITIVE_IMAGES_FOLDER) $(NEGATIVE_IMAGES_FOLDER)

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
		python3 scripts/confirm_positives.py

POSITIVE_AMOUNT := $(shell type positive_amount.tmp) #use on windows devices
NEGATIVE_AMOUNT := $(shell type negative_amount.tmp)

#POSITIVE_AMOUNT := $(shell cat positive_amount.tmp) # use on UNIX
#NEGATIVE_AMOUNT := $(shell cat negative_amount.tmp)

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
		-numStages 20

# Clear files
clean:
	-@ del /F $(POSITIVE_ANNOTATION_FILE)
	-@ del /F $(NEGATIVE_ANNOTATION_FILE)
	-@ del /F $(POSITIVE_VECTOR_FILE)
	-@ del /F negative_amount.tmp 
	-@ del /F positive_amount.tmp

	-@ rmdir /S /Q $(INPUT_FOLDER)
	-@ rmdir /S /Q $(OUTPUT_FOLDER)
	-@ rmdir /S /Q $(POSITIVE_IMAGES_FOLDER)
	-@ rmdir /S /Q $(NEGATIVE_IMAGES_FOLDER)

detect:
	@if not exist $(OUTPUT_FOLDER) mkdir $(OUTPUT_FOLDER)
	python3 scripts/check_images.py $(INPUT_FOLDER) $(OUTPUT_FOLDER)

webcam:
	python3 scripts/webcam.py
	
# Fully train the model from scratch
train: clean load_folders annotate vec
	@echo "POSITIVE_AMOUNT: $$(cat positive_amount.tmp)"
	@echo "NEGATIVE_AMOUNT: $$(cat negative_amount.tmp)"
	make train-s
	make clean
	@echo "$(GREEN)Model is trained! XML is ready for use$(RESET)"
	@if not exist $(INPUT_FOLDER) mkdir $(INPUT_FOLDER)
