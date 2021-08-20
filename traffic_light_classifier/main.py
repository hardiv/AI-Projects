from classifier import classify

# Set default directory for testing data
default_directory = "test_data/"
repeating = True

while repeating:
	# Get the input image from the user
	image = default_directory + input("\n\nFilename of image to test (X to exit): ") + ".jpg"
	if image.upper() == default_directory.upper() + "X.JPG":
		print("\nExited Successfully")
		repeating = False
		break
	print("\n(Ignore the following warnings, output will print on a newline):")
	# Classify the image
	image_label, highest_confidence = classify(image)

	# Output the classification
	print("\n" + image_label + " traffic light with " + str(round(highest_confidence * 100, 3)) + "% confidence")
