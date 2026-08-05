from PIL import Image, ImageFilter, ImageOps


class ImagePreprocessingService:

    def preprocess(
        self,
        image: Image.Image,
    ) -> Image.Image:
        """
        Prepare an image for OCR.
        """

        # Convert to grayscale
        image = ImageOps.grayscale(image)

        # Increase contrast automatically
        image = ImageOps.autocontrast(image)

        # Apply median filter to reduce noise
        image = image.filter(
            ImageFilter.MedianFilter(size=3)
        )

        return image


image_preprocessing_service = (
    ImagePreprocessingService()
)